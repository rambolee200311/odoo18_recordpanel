export async function loadPreview(orm, targetModel, targetResId) {
    return orm.call("wd.preview.configuration", "load_preview_data", [
        targetModel,
        targetResId,
    ]);
}
