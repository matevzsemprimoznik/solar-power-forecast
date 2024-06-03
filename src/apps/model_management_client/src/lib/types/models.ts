export interface Model {
  aliases: string[];
  creation_time: number;
  current_stage: string;
  description: string;
  last_updated_timestamp: number;
  name: string;
  run_id: string;
  run_link: string;
  source: string;
  status: string;
  status_message: string;
  tags: Record<string, any>;
  user_id: string;
  version: string;
}

export interface MoveModelToProductionData {
  name: string;
  version: string;
}
