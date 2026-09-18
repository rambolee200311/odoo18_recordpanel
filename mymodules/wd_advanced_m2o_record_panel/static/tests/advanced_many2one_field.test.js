import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { describe, expect, test } from "@odoo/hoot";
import {
    AdvancedMany2OneField,
    advancedMany2OneField,
} from "../src/fields/enhanced_many2one_field";
import { buildRecordNavigation } from "../src/navigation/record_navigation";

describe("advanced_many2one_field", () => {
    test("registers an independent advanced Many2one field", () => {
        expect(registry.category("fields").get("advanced_many2one")).toBe(
            advancedMany2OneField
        );
        expect(registry.category("fields").get("many2one")).not.toBe(advancedMany2OneField);
        expect(advancedMany2OneField.component).toBe(AdvancedMany2OneField);
    });

    test("resolves supported and unsupported opening modes", () => {
        const baseArgs = {
            attrs: {},
            context: {},
            decorations: {},
            string: "Partner",
            options: {},
        };
        const dynamicInfo = { context: {}, domain: [] };

        expect(advancedMany2OneField.extractProps(baseArgs, dynamicInfo).openMode).toBe(
            "native"
        );
        expect(
            advancedMany2OneField.extractProps(
                { ...baseArgs, options: { open_mode: "tab" } },
                dynamicInfo
            ).openMode
        ).toBe("tab");
        expect(
            advancedMany2OneField.extractProps(
                { ...baseArgs, options: { open_mode: "extend" } },
                dynamicInfo
            ).openMode
        ).toBe("extend");
        expect(
            advancedMany2OneField.extractProps(
                { ...baseArgs, options: { open_mode: "invalid" } },
                dynamicInfo
            ).openMode
        ).toBe("native");
    });

    test("builds a standard target record URL without an RPC", () => {
        expect(buildRecordNavigation("res.partner", 25)).toEqual({
            ok: true,
            url: "/odoo/res.partner/25",
        });
        expect(buildRecordNavigation("", 25)).toEqual({
            ok: false,
            reason: "missing_target_model",
        });
        expect(buildRecordNavigation("res.partner", 0)).toEqual({
            ok: false,
            reason: "invalid_target_res_id",
        });
    });

    test("opens tab mode synchronously and preserves the source field", () => {
        const opened = [];
        const unpatch = patch(browser, {
            open: (url, target) => {
                opened.push({ url, target });
                return {};
            },
        });
        try {
            AdvancedMany2OneField.prototype.openAction.call({
                openMode: "tab",
                relation: "res.partner",
                resId: 25,
                notification: { add: () => expect.step("unexpected warning") },
            });
        } finally {
            unpatch();
        }

        expect(opened).toEqual([{ url: "/odoo/res.partner/25", target: "_blank" }]);
        expect.verifySteps([]);
    });

    test("reports an invalid tab target without opening a window", () => {
        const warnings = [];
        const unpatch = patch(browser, {
            open: () => expect.step("unexpected browser open"),
        });
        try {
            AdvancedMany2OneField.prototype.openAction.call({
                openMode: "tab",
                relation: "res.partner",
                resId: undefined,
                notification: {
                    add: (message, options) => warnings.push({ message, options }),
                },
            });
        } finally {
            unpatch();
        }

        expect(warnings).toHaveLength(1);
        expect(warnings[0].options.type).toBe("warning");
        expect.verifySteps([]);
    });
});
