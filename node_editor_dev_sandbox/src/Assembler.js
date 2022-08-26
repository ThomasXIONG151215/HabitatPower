import { Node } from "@baklavajs/core";

export class AssemblerNode extends Node {
    constructor() {
        super();
        this.type = "Device";
        this.name = "Assembler";
        this.addOption("设备名称", "InputOption", "集能气");
        this.addOption("源数", "InputOption", 1);

        for (var i = 1; i < this.getOptionValue("源数"); i++) {
            this.addInputInterface("source", "NumberOption");
        }

        this.addOutputInterface("总质量", "NumberOption", 20);
    }

    //calculate() {
    //    const n1 = this.getInterface("进水温度").value;
    //    const n2 = this.getInterface("出水温度").value;
    //    const cold = this.getOptionValue("水泵频率");
    //    let result;
    //    result = n1 * n2 * cold;
    //    this.getInterface("泵功率").value = result;
    //}
}
