import { Node } from "@baklavajs/core";

export class SpaceNode extends Node {
    constructor() {
        super();
        this.type = "Environment";
        this.name = "Indoor Space";
        this.addOption("名称", "InputOption", "人聚集空间");
        this.addOption("总体积", "NumberOption", 1000);
        this.addOption("均值人流量", "NumberOption", 100);
        this.addOption("室内温度设定", "NumberOption", 24);
        this.addOption("热负荷结论", "NumberOption", 3000);
        this.addOption("排气量设定", "NumberOption", 2200);

        this.addOutputInterface("向外排气量", "NumberOption", 1200);

        this.addOption("是否满足热量需求", "CheckboxOption", "False");

        this.addInputInterface("围护体的风", "NumberOption");
        this.addInputInterface("围护体的热", "NumberOption");
        this.addInputInterface("系统的风", "NumberOption");
        this.addInputInterface("系统的热", "NumberOption");
    }
    calculate() {
        const n1 = this.getInterface("围护体的热").value;
        const n2 = this.getInterface("系统的热").value;
        let result;
        result = n1 + n2;
        if (result >= this.getOptionValue("热负荷结论")) {
            this.setOptionValue("是否满足热量需求", true);
        }
    }
}
