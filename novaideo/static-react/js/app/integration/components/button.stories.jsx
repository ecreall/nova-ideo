import React from 'react';
import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { withInfo } from '@storybook/addon-info';
import {
  select, withKnobs, text, boolean
} from '@storybook/addon-knobs';

import Button from '../../components/styledComponents/Button';

const colors = ['#4caf50', '#d72b3f'];

const playgroundButton = {
  label: 'Hello world',
  disabled: false,
  color: colors[0]
};

const actions = {
  onClickHandler: action('onClickHandler')
};

storiesOf('Button', module)
  .addDecorator(withKnobs)
  .add(
    'playground',
    withInfo()(() => {
      return (
        <Button
          disabled={boolean('isDisabled', playgroundButton.disabled)}
          background={select('background', colors)}
          onClickHandler={actions.onClickHandler}
        >
          {text('label', playgroundButton.label)}
        </Button>
      );
    })
  );