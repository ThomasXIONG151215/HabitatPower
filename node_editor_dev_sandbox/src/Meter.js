import { Node } from "@baklavajs/core";

export class MeterNode extends Node {
    constructor() {
        super();
        this.type = "Device";
        this.name = "Meter";
        this.addOption("名称", "InputOption", "电表");
        this.addInputInterface("能耗 1", "NumberOption", 400);
        this.addInputInterface("能耗 2", "NumberOption", 400);
        this.addOption("电价", "NumberOption", 20);
        this.addOption("瞬时成本", "NumberOption", 0);
    }
    calculate() {
        const n1 = this.getInterface("能耗 1").value;
        const n2 = this.getInterface("能耗 2").value;

        let result;
        result = n1 + n2;
        this.getInterface("瞬时成本").value = result;
    }
}
