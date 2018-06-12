export class NewRoomMessage {

    constructor() {
        this.tags = new Array<string>();
    }

    name: string;
    tags: Array<string>;
    number_of_questions: number;
}
