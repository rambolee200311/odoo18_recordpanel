from odoo import api, fields, models
from odoo.exceptions import ValidationError


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
