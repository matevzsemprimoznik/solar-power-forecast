'use client'
import { useParams } from 'next/navigation';
import { useModel } from '@/lib/hooks/use-model';
import LoadingView from '@/components/ui/loading-view';
import { useMemo } from 'react';
import { Model } from '@/lib/types/models';
import Image from 'next/image';
import { formatDate, pretifyString } from '@/lib/utils';

export default function ModelPage() {
  const { id } = useParams()
  const { data, isLoading } = useModel(id as string, {
    enabled: !!id
  })
  const dataBasicSection = useMemo(() => {
    if (!data) return null;
    return {
      id: data.id,
      name: data.name,
      version: data?.version,
      created: formatDate(data.creation_time),
      updated: formatDate(data.last_updated_timestamp),
      description: data.description,
      userId: data.user_id,
      source: data.source,
      runId: data.run_id,
      runLink: data.run_link,
      status: data.status,
      statusMessage: data.status_message,
      aliases: data.aliases.join(', '),
    }
  }, [data])

  return (
    <div className='h-full p-10'>
      <LoadingView isLoading={isLoading}>
        {data && <><h1 className='text-3xl mb-10'>{pretifyString(data.name)}</h1>
          <div className='grid grid-cols-2 gap-y-5'>
            {dataBasicSection && Object.entries(dataBasicSection).map(([key, value]) => <div key={key} className='flex'>
              <div className='grid grid-cols-[140px_1fr] w-full max-w-full'>
                <div className="font-bold w-full break-words">{pretifyString(key)}</div>
                <div className="break-words max-w-[350px]">{value || '/'}</div>
              </div>
            </div>)}
          </div>
          <h2 className='text-xl mt-20 mb-5'>Artifacts</h2>
        {data?.artifacts.shap_bar ? <div className='grid grid-cols-2 gap-x-10'>
            <div className='relative w-full' style={{ paddingBottom: "70%" }}>
              <Image layout="fill"
                     objectFit="contain" src={`data:image/png;base64,${data?.artifacts.shap_bar}`}
                     alt={'Snap Bar Chart'} />
            </div>
            <div className='relative w-full'>
              <Image layout="fill"
                     objectFit="contain" src={`data:image/png;base64,${data?.artifacts.shap_beeswarm}`}
                     alt={'Snap BeeSwarm Chart'} />
            </div>
        </div> : <div className=''>No artifacts found for this model</div>
        }
        </>}
        </LoadingView>
          </div>
          );
        }