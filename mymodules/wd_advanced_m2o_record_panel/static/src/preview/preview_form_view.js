import { registry } from "@web/core/registry";
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { PreviewHost } from "./preview_host";

class PreviewFormController extends FormController {
    static template = "web.FormView";
    static components = { ...FormController.components, PreviewHost };
}

registry.category("views").add(
    "form",
    {
        ...formView,
        Controller: PreviewFormController,
    },
    { force: true }
);
