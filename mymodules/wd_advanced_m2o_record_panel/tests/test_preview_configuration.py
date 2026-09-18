from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import TransactionCase


class TestPreviewConfiguration(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.configuration_model = cls.env["wd.preview.configuration"]
        cls.line_model = cls.env["wd.preview.configuration.line"]
        cls.partner_model = cls.env["ir.model"]._get("res.partner")
        cls.company_model = cls.env["ir.model"]._get("res.company")
        cls.partner_name_field = cls.env["ir.model.fields"]._get(
            "res.partner", "name"
        )
        cls.company_name_field = cls.env["ir.model.fields"]._get(
            "res.company", "name"
        )

    def test_one_configuration_per_target_model_even_when_inactive(self):
        self.configuration_model.create(
            {"target_model_id": self.partner_model.id, "active": False}
        )
        with self.assertRaises(Exception):
            self.configuration_model.create(
                {"target_model_id": self.partner_model.id, "active": True}
            )

    def test_line_must_belong_to_target_model(self):
        configuration = self.configuration_model.create(
            {"target_model_id": self.partner_model.id}
        )
        with self.assertRaises(ValidationError):
            self.line_model.create(
                {
                    "configuration_id": configuration.id,
                    "field_id": self.company_name_field.id,
                }
            )

    def test_duplicate_field_is_rejected(self):
        configuration = self.configuration_model.create(
            {"target_model_id": self.partner_model.id}
        )
        self.line_model.create(
            {
                "configuration_id": configuration.id,
                "field_id": self.partner_name_field.id,
            }
        )
        with self.assertRaises(Exception):
            self.line_model.create(
                {
                    "configuration_id": configuration.id,
                    "field_id": self.partner_name_field.id,
                }
            )

    def test_target_model_cannot_change_with_lines(self):
        configuration = self.configuration_model.create(
            {"target_model_id": self.partner_model.id}
        )
        self.line_model.create(
            {
                "configuration_id": configuration.id,
                "field_id": self.partner_name_field.id,
            }
        )
        with self.assertRaises(ValidationError):
            configuration.write({"target_model_id": self.company_model.id})

    def test_configuration_line_order_is_deterministic(self):
        configuration = self.configuration_model.create(
            {"target_model_id": self.partner_model.id}
        )
        first = self.line_model.create(
            {
                "configuration_id": configuration.id,
                "field_id": self.partner_name_field.id,
                "sequence": 20,
            }
        )
        second = self.line_model.create(
            {
                "configuration_id": configuration.id,
                "field_id": self.env["ir.model.fields"]._get(
                    "res.partner", "email"
                ).id,
                "sequence": 10,
            }
        )
        ordered_lines = self.line_model.search(
            [("configuration_id", "=", configuration.id)]
        )
        self.assertEqual(ordered_lines.ids, [second.id, first.id])

    def test_internal_user_can_read_but_not_write_configuration(self):
        user = self.env.ref("base.user_demo")
        configuration = self.configuration_model.create(
            {"target_model_id": self.partner_model.id}
        )
        user_configuration = configuration.with_user(user)
        self.assertEqual(user_configuration.read(["target_model_id"])[0]["id"], configuration.id)
        with self.assertRaises(AccessError):
            user_configuration.write({"active": False})
