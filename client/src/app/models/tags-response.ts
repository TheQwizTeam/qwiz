import { Tag } from './tag';

export interface TagsResponse {
    count: number;
    prev: any;
    next: any;
    results: Array<Tag>
}
