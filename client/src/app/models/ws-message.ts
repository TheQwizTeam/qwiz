export class WsMessage {

    constructor(command: string, room_code: string, contestant_name: string) {
        this.command = command;
        this.room_code = room_code;
        this.contestant_name = contestant_name;
    }

    command: string;
    room_code: string;
    contestant_name: string;
    contestants: string[];
}