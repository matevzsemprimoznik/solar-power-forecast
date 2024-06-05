import { modelsManagementApi } from '@/lib/api/axios';
import axios from 'axios';
import { Model, MoveModelToProductionData } from '@/lib/types/models';

export const getModels = async () => {
    const {data} = await modelsManagementApi.get('/models');
    return data as Model[];
}

export const moveModelToProduction = async (input: MoveModelToProductionData) => {
    const {data} = await modelsManagementApi.post(`/models/production/name/${input.name}/version/${input.version}`);
    return data;
}

export const getModel = async (id: string) => {
    const {data} = await modelsManagementApi.get(`/models/${id}`);
    return data as Model;
}

export const trainModel = async (modelName: string) => {
    const {data} = await modelsManagementApi.post(`/models/train/${modelName}`);
    return data;
}
