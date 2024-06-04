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

export default function Home() {
  const {data: models, isLoading} = useModels();
  const {addListener} = useEventDispatcher();
  const queryClient = useQueryClient();
  const { toast, dismiss } = useToast()
  const [toastId, setToastId
  ] = useState('')

  const {mutateAsync: moveModelToProduction} = useMoveModelToProduction({
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: modelsKeys.all
      });
      console.log(toastId);
      dismiss(toastId);
    }
  })

  const tableData = useMemo(() => {
    if (!models) return [];
    return models.map(model => ({
      ...model,
      'metric-evs': model.metrics['Explained Variance Score'].toFixed(3),
      'metric-mae': model.metrics['Mean Absolute Error'].toFixed(3),
      'metric-mse': model.metrics['Mean Squared Error'].toFixed(3),
    }))
  }, [models])



  useEffect(() => {
    addListener('move-model-to-production-event', async (data) => {
      console.log('Moving model to production from dispatch');
      setTimeout(() => {
        const t = toast({
          duration: 1000000,
          title: 'Model Management',
          description: <div className='flex justify-center items-center bg-white dark:invert'>
            <span className='mr-1'>Moving model to production </span>
            <span className='animate-bounce [animation-delay:-0.3s] ml-0 font-bold'>.</span>
            <span className='animate-bounce [animation-delay:-0.15s] ml-0 font-bold'>.</span>
            <span className='animate-bounce ml-0 font-bold'>.</span>
          </div>
        })
        setToastId(t.id)
      }, 0)
      await moveModelToProduction(data);
    });
  }, [addListener]);


  return (
    <div className="p-10">
      <h1 className="text-3xl mb-10">Model Management App</h1>
      <LoadingView isLoading={isLoading}>
        <DataTable columns={columns} data={tableData} />
      </LoadingView>
    </div>
  );
}
