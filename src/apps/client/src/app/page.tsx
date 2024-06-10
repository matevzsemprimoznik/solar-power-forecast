'use client';
import { usePredictions } from '@/lib/hooks/use-predictions';
import React, { useMemo } from 'react';
import PowerCard from '@/components/ui/power-card';
import Section from '@/components/ui/section';
import { covertToBestUnit, dateToString, getCurrentUtcDate } from '@/utils';
import { useHistory } from '@/lib/hooks/use-history';
import {
  Brush,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  LineChart,
  ReferenceArea,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { format, parseISO } from 'date-fns';
import { usePredictionHistory } from '@/lib/hooks/use-prediction-history';
import { PredictionHistory } from '@/lib/types/prediction';

const currentDateUtc = getCurrentUtcDate();
const yesterdayStartDate = new Date(currentDateUtc);
yesterdayStartDate.setDate(yesterdayStartDate.getDate() - 1);
yesterdayStartDate.setHours(0, 0, 0, 0);

const yesterdayEndDate = new Date(yesterdayStartDate);
yesterdayEndDate.setHours(23, 59, 59, 999);

const lastWeekStartDate = new Date(currentDateUtc);
lastWeekStartDate.setDate(lastWeekStartDate.getDate() - 7);

const lastWeekEndDate = new Date(lastWeekStartDate);
lastWeekEndDate.setHours(23, 59, 59, 999);
lastWeekEndDate.setDate(lastWeekEndDate.getDate() + 7);

export default function Home() {
  const { data: predictions } = usePredictions();
  const { data: productionYesterday } = useHistory(
    dateToString(yesterdayStartDate),
    dateToString(yesterdayEndDate)
  );
  const { data: predictionHistory } = usePredictionHistory();

  const { data: productionLastWeek } = useHistory(
    dateToString(lastWeekStartDate),
    dateToString(lastWeekEndDate)
  );

  const totalYesterday = useMemo(() => {
    if (!productionYesterday) return 0;
    return productionYesterday.reduce(
      (acc, production) => acc + production.power,
      0
    );
  }, [productionYesterday]);

  const totalLastWeek = useMemo(() => {
    if (!productionLastWeek) return 0;
    return productionLastWeek.reduce(
      (acc, production) => acc + production.power,
      0
    );
  }, [productionLastWeek]);

  const nextHourPrediction = useMemo(() => {
    return predictions && predictions?.length !== 0
      ? predictions[0].prediction
      : 0;
  }, [predictions]);

  const totalNextDay = useMemo(() => {
    if (!predictions || predictions.length === 0) return 0;
    let nextDayStart = new Date();
    nextDayStart.setHours(0, 0, 0, 0);
    nextDayStart.setDate(nextDayStart.getDate() + 1);

    let nextDayEnd = new Date(nextDayStart);
    nextDayEnd.setHours(23, 59, 59, 999);

    const nextDayPredictions = predictions.filter((prediction) => {
      const predictionDate = new Date(prediction.date);
      return predictionDate >= nextDayStart && predictionDate <= nextDayEnd;
    });
    return nextDayPredictions.reduce(
      (acc, prediction) => acc + prediction.prediction,
      0
    );
  }, [predictions]);

  const production = useMemo(() => {
    if (!productionLastWeek || !predictions || !predictionHistory) return [];
    const pred = [...predictionHistory, ...predictions] as unknown as {
      date: Date;
      power?: number;
      prediction: number;
    }[];

    const targetDate = new Date();
    targetDate.setHours(targetDate.getHours() + 2, 0, 0, 0);

    return pred.map((p) => ({
      date: p.date.getTime(),
      day: `${p.date.getDate()}/${p.date.getMonth() + 1}`,
      power: p.power != null ? (p.power / 1000000).toFixed(2) : null,
      prediction: (p.prediction / 1000000).toFixed(2),
    }));
  }, [productionLastWeek, predictions, predictionHistory]);

  const startBrushIndex = useMemo(() => {
    const currentTime = getCurrentUtcDate();
    return production.findIndex((p) => p.date >= currentTime.getTime()) - 5;
  }, [production]);

  return (
    <div className='w-full h-full bg-neutral-light p-10'>
      <h1 className='text-2xl font-bold'>E.W. Brown Solar Facility</h1>
      <Section title='Summary'>
        <div className='flex gap-3'>
          <PowerCard
            className='w-full border-2 border-tint-secondary'
            title='Next Hour:'
            value={covertToBestUnit(nextHourPrediction, 'W')}
          />
          <PowerCard
            className='w-full border-2 border-tint-secondary'
            title='Tommorow:'
            value={covertToBestUnit(totalNextDay, 'Wh')}
          />
          <PowerCard
            className='w-full border-2 border-tint'
            title='Yesterday:'
            value={covertToBestUnit(totalYesterday, 'Wh')}
          />
          <PowerCard
            className='w-full border-2 border-tint'
            title='Last Week:'
            value={covertToBestUnit(totalLastWeek, 'Wh')}
          />
        </div>
      </Section>
      <Section title='Production Chart'>
        <ResponsiveContainer width='100%' height={600}>
          <ComposedChart
            data={production}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray='3 3' />
            <XAxis
              xAxisId={0}
              dataKey='date'
              type='number'
              domain={['dataMin', 'dataMax']}
              scale={'time'}
              tickFormatter={(tick) => format(new Date(tick), 'HH:mm')}
            />
            <XAxis xAxisId={1} dataKey='day' interval={5} />

            <YAxis tickFormatter={(tick) => tick + ' MW'} />
            <Tooltip
              labelFormatter={(label) => format(new Date(label), 'MM/dd HH:mm')}
              formatter={(value) => value + ' MW'}
            />
            <Legend />
            <Line
              type='monotone'
              dataKey='power'
              stroke='#8884d8'
              activeDot={{ r: 8 }}
              xAxisId={0}
              strokeWidth={2}
            />
            <Line
              type='monotone'
              dataKey='prediction'
              stroke='#80ed99'
              activeDot={{ r: 8 }}
              xAxisId={0}
              strokeWidth={2}
            />
            <ReferenceLine x={new Date().getTime()} label={'Current Time'} />
            <Brush
              dataKey='power'
              height={30}
              stroke='#8884d8'
              startIndex={startBrushIndex}
              endIndex={startBrushIndex + 10}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </Section>
    </div>
  );
}
