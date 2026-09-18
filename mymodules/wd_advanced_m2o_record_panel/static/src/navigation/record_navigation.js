import { router } from "@web/core/browser/router";

function isPositiveInteger(value) {
    return Number.isInteger(value) && value > 0;
}

export function buildRecordNavigation(targetModel, targetResId) {
    if (typeof targetModel !== "string" || !targetModel.trim()) {
        return { ok: false, reason: "missing_target_model" };
    }
    if (!isPositiveInteger(targetResId)) {
        return { ok: false, reason: "invalid_target_res_id" };
    }
    return {
        ok: true,
        url: router.stateToUrl({
            model: targetModel,
            resId: targetResId,
        }),
    };
}
