import React from 'react';
import { BaseProps } from '../@types/common';
import { PiQuestionFill } from 'react-icons/pi';
import Tooltip from './Tooltip';
import { Direction } from '../constants';

type Props = BaseProps & {
  message: string;
  direction?: Direction;
};

const Help: React.FC<Props> = (props) => {
  return (
    <Tooltip {...props}>
      <PiQuestionFill />
    </Tooltip>
  );
};

export default Help;
