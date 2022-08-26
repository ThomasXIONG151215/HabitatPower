import { Node } from "@baklavajs/core";

export class FanNode extends Node {
    constructor() {
        super();
        this.type = "Device";
        this.name = "Fan";
        this.addOption("设备名称", "InputOption", "风机");
        this.addOption("风机频率", "NumberOption", 100);
        this.addOption("尺寸", "NumberOption", 0.8);
        this.addOption("设计风机流速", "NumberOption", 24);

        this.addInputInterface("室外空气温度", "NumberOption", 1);
        this.addInputInterface("进水温度", "NumberOption", 1);

        this.addOption("室外空气饱和温度", "NumberOption", 1);
        this.addOption("室外空气焓", "NumberOption", 1);
        this.addOption("室外空气饱和焓", "NumberOption", 1);

        //this.addOption("Operation", "SelectOption", "Add", undefined, {
        //  items: ["Add", "Subtract"]
        //});
        this.addOutputInterface("出风温度", "NumberOption", 31);
        this.addOutputInterface("出风流速", "NumberOption", 18);
        this.addOutputInterface("风机功率", "NumberOption", 220);
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
