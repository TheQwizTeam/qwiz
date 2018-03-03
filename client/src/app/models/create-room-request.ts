import { Tag } from './tag';

export class CreateRoomRequest {

    constructor() {
        this.tags = new Array<Tag>();
    }

    num_questions: number;
    name: string;
    tags: Array<Tag>
}
