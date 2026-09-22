from odoo import api, fields, models
from odoo.exceptions import AccessError, MissingError, ValidationError


class PreviewConfiguration(models.Model):
    _name = "wd.preview.configuration"
    _description = "Many2one Preview Configuration"
    _rec_name = "name"

    name = fields.Char(compute="_compute_name", store=True)
    target_model_id = fields.Many2one(
        "ir.model",
        string="Target Model",
        required=True,
        ondelete="cascade",
    )
    active = fields.Boolean(default=True)
    line_ids = fields.One2many(
        "wd.preview.configuration.line",
        "configuration_id",
        string="Preview Fields",
    )

    _sql_constraints = [
        (
            "target_model_unique",
            "unique(target_model_id)",
            "Only one Preview Configuration is allowed per target model.",
        ),
    ]

    @api.depends("target_model_id.name")
    def _compute_name(self):
        for configuration in self:
            configuration.name = configuration.target_model_id.name or False

    @api.constrains("target_model_id", "line_ids")
    def _check_line_models(self):
        for configuration in self:
            invalid_lines = configuration.line_ids.filtered(
                lambda line: line.field_id.model != configuration.target_model_id.model
            )
            if invalid_lines:
                raise ValidationError(
                    "Every preview field must belong to the configured target model."
                )

    def write(self, vals):
        if "target_model_id" in vals:
            for configuration in self:
                if configuration.line_ids and configuration.target_model_id.id != vals["target_model_id"]:
                    raise ValidationError(
                        "Remove preview fields before changing the target model."
                    )
        return super().write(vals)

    @api.model
    def load_preview_data(self, target_model, target_res_id):
        """Return only data the current user may read for a configured target."""
        if not isinstance(target_model, str) or not target_model.strip():
            return {"status": "access_denied", "code": "invalid_target"}
        if isinstance(target_res_id, str) and target_res_id.isdecimal():
            target_res_id = int(target_res_id)
        if isinstance(target_res_id, bool) or not isinstance(target_res_id, int):
            return {"status": "access_denied", "code": "invalid_target"}
        try:
            target = self.env[target_model].browse(target_res_id)
        except KeyError:
            return {"status": "access_denied", "code": "invalid_target"}
        if not target.exists():
            return {"status": "access_denied", "code": "access_denied"}
        try:
            target.check_access_rights("read")
            target.check_access_rule("read")
        except (AccessError, MissingError):
            return {"status": "access_denied", "code": "access_denied"}

        try:
            configuration = self.search(
                [("active", "=", True), ("target_model_id.model", "=", target_model)],
                limit=1,
            )
        except AccessError:
            configuration = self.browse()

        try:
            identity = {
                "model": target_model,
                "resId": target.id,
                "displayName": target.display_name,
            }
        except (AccessError, MissingError):
            return {"status": "access_denied", "code": "access_denied"}
        if not configuration:
            return {
                "status": "fallback",
                "target": identity,
                "message": "No preview fields are configured for this record.",
                "code": "no_configuration",
            }

        rows = []
        for line in configuration.line_ids.sorted("sequence"):
            field_name = line.field_id.name
            field = target._fields.get(field_name)
            if not field:
                continue
            try:
                target.check_field_access_rights("read", [field_name])
                value = target.read([field_name], load=False)[0][field_name]
                value = self._serialize_preview_value(target[field_name], field, value)
                rows.append({
                    "name": field_name,
                    "label": line.field_id.field_description,
                    "value": value,
                })
            except (AccessError, KeyError, MissingError, ValueError):
                continue
        if not rows:
            return {
                "status": "fallback",
                "target": identity,
                "message": "No readable preview fields are configured for this record.",
                "code": "no_readable_fields",
            }
        return {"status": "ready", "target": identity, "rows": rows}

    @staticmethod
    def _serialize_preview_value(record_value, field, raw_value):
        if raw_value is None:
            return None
        if field.type == "many2one":
            return record_value.display_name if record_value else False
        if field.type in {"many2many", "one2many"}:
            return ", ".join(record_value.mapped("display_name"))
        if field.type in {"char", "text", "html", "selection", "date", "datetime"}:
            return str(raw_value)
        if field.type in {"integer", "float", "monetary", "boolean"}:
            return raw_value
        return str(raw_value)
