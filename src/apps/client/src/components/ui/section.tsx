import { ReactNode } from 'react';

interface SectionProps {
  title: string;
  children: ReactNode;
}
export default function Section({ children, title }: SectionProps) {
  return (
    <div className='py-8'>
      <p className='font-bold text-lg mb-3'>{title}</p>
      {children}
    </div>
  );
}
