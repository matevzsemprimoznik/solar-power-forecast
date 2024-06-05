'use client'
import { useModels } from '@/lib/hooks/use-models';
import { DataTable } from '@/components/ui/data-table';
import { columns } from '@/components/ui/data-table-columns';
import LoadingView from '@/components/ui/loading-view';
import { useEventDispatcher } from '@/lib/hooks/use-event-dispatcher';
import { useEffect, useMemo, useState } from 'react';
import { useMoveModelToProduction } from '@/lib/hooks/use-move-model-to-production';
import { useQueryClient } from '@tanstack/react-query';
import { modelsKeys } from '@/lib/hooks/key-factories';
import { useToast } from '@/components/ui/use-toast';
import { useModelTrain } from '@/lib/hooks/use-model-train';
import { Model } from '@/lib/types/models';
import CustomModalDescription from '@/components/ui/custom-modal';
import { pusherClient } from '@/lib/utils';
import { channel } from 'node:diagnostics_channel';

export default function Home() {
  const {data: models, isLoading} = useModels();
  const {addListener, removeListener} = useEventDispatcher();
  const queryClient = useQueryClient();
  const { toast } = useToast()
  const {mutateAsync: moveModelToProduction} = useMoveModelToProduction({
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: modelsKeys.all
      });
      toast({
        title: 'Model Move to Production',
        description: 'Model is moving to production. This may take a while. You will be notified when the model is in production.'
      })
    }
  })
  const {mutateAsync: trainModel} = useModelTrain({
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: modelsKeys.all
      });
      toast({
        title: 'Model Train',
        description: 'Your model is being trained. This may take a while. You will be notified when the training is complete.'
      })
    }
  })

  const tableData = useMemo(() => {
    if (!models) return [];
    return models.map(model => ({
      ...model,
      'metric-evs': model.metrics['evs'].toFixed(3),
      'metric-mae': model.metrics['mae'].toFixed(3),
      'metric-mse': model.metrics['mse'].toFixed(3),
    }))
  }, [models])



  useEffect(() => {
    const moveModelToProductionListener = async (data: Model) => {
      await moveModelToProduction(data);
    }
    const trainModelListener = async (data: Model) => {
      await trainModel(data.name);
    }

    addListener('move-models-to-production-event', moveModelToProductionListener);
    addListener('train-model', trainModelListener)

    return () => {
      removeListener('move-models-to-production-event', moveModelToProductionListener);
      removeListener('train-model', trainModelListener);
    }
  }, [addListener]);

  useEffect(() => {
    const solarPowerModelManagerChannel = pusherClient.subscribe('solar-power-model-management-api');
    solarPowerModelManagerChannel.bind('model-trained-successfully', async (data: any) => {
      toast({
        title: 'Model Trained',
        description: data.message
      })
      await queryClient.invalidateQueries({
        queryKey: modelsKeys.all
      });
    })
    solarPowerModelManagerChannel.bind('model-moved-to-production-successfully', async (data: any) => {
      toast({
        title: 'Model moved to Production',
        description: data.message
      })
      await queryClient.invalidateQueries({
        queryKey: modelsKeys.all
      });
    })
  }, []);


  return (
    <div className="p-10 h-full">
      <h1 className="text-3xl mb-10">Model Management App</h1>
      <LoadingView isLoading={isLoading}>
        <DataTable columns={columns} data={tableData} />
      </LoadingView>
    </div>
  );
}
