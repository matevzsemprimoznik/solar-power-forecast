import { cn } from '@/utils';

interface CardProps {
  title: string;
  value: string;
  className?: string;
}
export default function PowerCard({ title, value, className }: CardProps) {
  return (
    <div
      className={cn(
        'bg-white h-44 shadow-sm rounded-lg p-4 flex flex-col items-center justify-center',
        className
      )}
    >
      <p className='font-bold text-lg'>{title}</p>
      <p>{value}</p>
    </div>
  );
}
