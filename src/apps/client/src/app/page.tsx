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
  Legend,
  Line,
  LineChart,
  ReferenceArea,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

const pdata = [
  {
    name: 'MongoDb',
    student: 11,
    fees: 120,
  },
  {
    name: 'Javascript',
    student: 15,
    fees: 12,
  },
  {
    name: 'PHP',
    student: 5,
    fees: 10,
  },
  {
    name: 'Java',
    student: 10,
    fees: 5,
  },
  {
    name: 'C#',
    student: 9,
    fees: 4,
  },
  {
    name: 'C++',
    student: 10,
    fees: 8,
  },
];

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
lastWeekEndDate.setDate(lastWeekEndDate.getDate() + 6);

export default function Home() {
  const { data: predictions } = usePredictions();
  const { data: productionYesterday } = useHistory(
    dateToString(yesterdayStartDate),
    dateToString(yesterdayEndDate)
  );

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
    return predictions && predictions?.length !== 0 ? predictions[0].power : 0;
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
      (acc, prediction) => acc + prediction.power,
      0
    );
  }, [predictions]);

  const production = useMemo(() => {
    if (!productionLastWeek || !predictions) return [];
    const merged = [...productionLastWeek, ...predictions];
    return merged.map(({ date, power }) => ({
      date: date.getTime(),
      day: `${date.getDate()}/${date.getMonth() + 1}`,
      hour: `${date.getHours()}:00`,
      power: power / 1000000,
    }));
  }, [productionLastWeek, predictions]);

  const startBrushIndex = useMemo(() => {
    const currentTime = getCurrentUtcDate();
    return production.findIndex((p) => p.date >= currentTime.getTime()) - 5;
  }, [production]);

  const referenceAreaRange = useMemo(() => {
    const currentTime = getCurrentUtcDate();
    const start = new Date(currentTime);
    start.setHours(start.getHours(), 0, 0, 0);

    const end = new Date(start);
    end.setHours(end.getHours() + 1);
    return { start: start.getTime(), end: end.getTime() };
  }, []);

  console.log(referenceAreaRange);

  return (
    <div className='w-full h-full bg-neutral-light p-10'>
      <h1 className='text-2xl font-bold'>E.W. Brown Solar Facility</h1>
      <Section title='Summary'>
        <div className='flex gap-3'>
          <PowerCard
            className='w-full'
            title='Next Hour:'
            value={covertToBestUnit(nextHourPrediction, 'W')}
          />
          <PowerCard
            className='w-full'
            title='Tommorow:'
            value={covertToBestUnit(totalNextDay, 'Wh')}
          />
          <PowerCard
            className='w-full'
            title='Yesterday:'
            value={covertToBestUnit(totalYesterday, 'Wh')}
          />
          <PowerCard
            className='w-full'
            title='Last Week:'
            value={covertToBestUnit(totalLastWeek, 'Wh')}
          />
        </div>
      </Section>
      <Section title='Production Chart'>
        <ResponsiveContainer
          width='100%'
          aspect={2.5}
          className='bg-white  shadow-sm rounded-lg p-4'
        >
          <LineChart
            width={500}
            height={300}
            data={production}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray='3 3' />
            <XAxis
              xAxisId={0}
              dy={0}
              dataKey='date'
              interval={0}
              minTickGap={100}
              tickLine={false}
              hide
            />
            <XAxis
              xAxisId={1}
              dy={0}
              dataKey='hour'
              interval={0}
              minTickGap={100}
              tickLine={false}
            />
            <XAxis
              xAxisId={2}
              dy={0}
              dataKey='day'
              interval={24}
              tickLine={false}
            />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type='monotone'
              dataKey='power'
              stroke='#8884d8'
              activeDot={{ r: 8 }}
              xAxisId={0}
            />
            <ReferenceArea
              xAxisId={0}
              x1={referenceAreaRange.start}
              x2={referenceAreaRange.end}
              label='Current Time'
              className='bg-white'
              fill={'rgba(136,132,216,0.12)'}
            />
            <Brush
              dataKey='power'
              height={30}
              stroke='#8884d8'
              startIndex={startBrushIndex}
              endIndex={startBrushIndex + 10}
            />
          </LineChart>
        </ResponsiveContainer>
      </Section>
    </div>
  );
}
