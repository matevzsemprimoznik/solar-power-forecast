import { modelsManagementApi } from '@/lib/api/axios';
import axios from 'axios';
import { MoveModelToProductionData } from '@/lib/types/models';

export const getModels = async () => {
    const {data} = await modelsManagementApi.get('/models');
    return data;
}

export const moveModelToProduction = async (input: MoveModelToProductionData) => {
    const {data} = await modelsManagementApi.post(`/models/production/name/${input.name}/version/${input.version}`);
    return data;
}
