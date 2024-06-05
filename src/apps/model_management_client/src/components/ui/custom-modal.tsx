interface CustomModalDescriptionProps {
  description: string
}
export default function CustomModalDescription({description}: CustomModalDescriptionProps) {
  return <div className='flex justify-center items-center bg-white dark:invert'>
    <span className='mr-1'>{description}</span>
    <span className='animate-bounce [animation-delay:-0.3s] ml-0 font-bold'>.</span>
    <span className='animate-bounce [animation-delay:-0.15s] ml-0 font-bold'>.</span>
    <span className='animate-bounce ml-0 font-bold'>.</span>
  </div>
}
