import { Node } from "@baklavajs/core";

export class SunNode extends Node {
    constructor() {
        super();
        this.type = "Environment";
        this.name = "Sun";
        this.addOption("名称", "InputOption", "太阳");
        this.addOption("照射方向", "SelectOption", "南", undefined, {
            items: ["南", "北", "东", "西"]
        });
        this.addOutputInterface("辐照值", "NumberOption", 400);
        this.addOutputInterface("亮度", "NumberOption", 20);
    }
}
