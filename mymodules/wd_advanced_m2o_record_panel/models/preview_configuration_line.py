from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PreviewConfigurationLine(models.Model):
    _name = "wd.preview.configuration.line"
    _description = "Many2one Preview Configuration Field"
    _order = "sequence, id"

    configuration_id = fields.Many2one(
        "wd.preview.configuration",
        required=True,
        ondelete="cascade",
    )
    field_id = fields.Many2one(
        "ir.model.fields",
        string="Field",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        (
            "configuration_field_unique",
            "unique(configuration_id, field_id)",
            "A field can only be configured once.",
        ),
    ]

    @api.constrains("configuration_id", "field_id")
    def _check_field_model(self):
        for line in self:
            if (
                line.configuration_id.target_model_id
                and line.field_id.model != line.configuration_id.target_model_id.model
            ):
                raise ValidationError(
                    "The preview field must belong to the configured target model."
                )
