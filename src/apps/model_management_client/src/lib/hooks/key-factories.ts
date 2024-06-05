export const modelsKeys = {
  all: ['models'],
  getById: (id: string) => ['models', id],
  moveToProduction: () => [modelsKeys.all, 'moveToProduction'],
  train: ['train']
}