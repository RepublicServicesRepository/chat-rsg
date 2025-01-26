import { TooltipDirection } from '../constants';
import Help from './Help';

export const Right = () => (
  <Help direction={TooltipDirection.RIGHT} message={'sample'} />
);

export const Left = () => (
  <div>
    <Help direction={TooltipDirection.LEFT} message={'sample'} />
  </div>
);
