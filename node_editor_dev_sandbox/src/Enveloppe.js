import { Node } from "@baklavajs/core";

export class EnveloppeNode extends Node {
    constructor() {
        super();
        this.type = "Structure";
        this.name = "Enveloppe";
        this.addOption("名称", "InputOption", "围护体");
        this.addOption("材料数目", "SelectOption", "1", undefined, {
            items: ["1", "2", "3", "4"]
        });

        this.addOption("材质1材料", "SelectOption", "A", undefined, {
            items: ["A", "B", "C", "D"]
        });
        this.addOption("材质1厚度", "NumberOption", 3);

        this.addInputInterface("室外热量传递", "NumberOption", 200);
        this.addOption("是否有窗户", "CheckboxOption");

        this.addOutputInterface("热量瞬时传递量", "NumberOption", 400);
        this.addOutputInterface("风量传入", "NumberOption", 20);
    }
    calculate() {
        if (this.getOptionValue("是否有窗户") === true) {
            this.addInputInterface("室外风量传入", "NumberOption", 200);
        }
    }
}
