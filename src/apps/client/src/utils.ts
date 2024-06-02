import { twMerge } from 'tailwind-merge';
import { ClassValue, clsx } from 'clsx';

export function covertToBestUnit(valueInWatts: number, baseUnit: string) {
  const units = [baseUnit, `k${baseUnit}`, `M${baseUnit}`, `G${baseUnit}`];
  let unitIndex = 0;

  while (valueInWatts >= 1000 && unitIndex < units.length - 1) {
    valueInWatts /= 1000;
    unitIndex++;
  }

  return valueInWatts.toFixed(0) + ' ' + units[unitIndex];
}

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function convertStringToDate(dateString: string) {
  const d = new Date(dateString);
  return new Date(
    Date.UTC(
      d.getUTCFullYear(),
      d.getUTCMonth(),
      d.getUTCDate(),
      d.getUTCHours(),
      d.getUTCMinutes(),
      d.getUTCSeconds(),
      d.getUTCMilliseconds()
    )
  );
}

export function getCurrentUtcDate() {
  const d = new Date();
  return new Date(
    Date.UTC(
      d.getUTCFullYear(),
      d.getUTCMonth(),
      d.getUTCDate(),
      d.getUTCHours(),
      d.getUTCMinutes(),
      d.getUTCSeconds(),
      d.getUTCMilliseconds()
    )
  );
}

export function dateToString(date: Date) {
  return `${date.getFullYear()}-${
    date.getMonth() + 1
  }-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
}

export function formatDateForChart(date: Date) {
  return `${date.getDate()}/${
    date.getMonth() + 1
  } ${date.getHours()}:${date.getMinutes()}`;
}
