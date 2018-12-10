import React from 'react';
import 'rc-slider/assets/index.css';
import Slider from 'rc-slider';
import Moment from 'moment';
import { withStyles } from '@material-ui/core/styles';

import DeadLineBtn from './DeadLineBtn';

const styles = {
  root: {
    flexGrow: 1
  },
  slider: {
    backgroundColor: 'transparent !important',
    height: '0 !important',
    padding: '0 !important'
  }
};

const getHandle = (date, isExpired, color) => {
  return (props) => {
    return <DeadLineBtn {...props} date={date} isExpired={isExpired} color={color} />;
  };
};

class ExaminationProgress extends React.Component {
  render() {
    const { classes, theme, values } = this.props;
    const today = Moment();
    const lastExamination = values[values.length - 1];
    let value = 1;
    let isExpired = false;
    let end = null;
    if (lastExamination) {
      const start = Moment(lastExamination.start);
      end = Moment(lastExamination.end);
      const total = end - start;
      const current = today - start;
      value = current * 100 / total;
      value = value === Infinity ? 100 : value;
      value = value > 100 || value < 0 ? 100 : value;
      isExpired = today >= end;
    }
    const sliderColor = isExpired ? theme.palette.danger.primary : theme.palette.tertiary.color;
    return (
      <div className={classes.root}>
        <Slider
          key={value}
          disabled
          handle={getHandle(end, isExpired, sliderColor)}
          min={-1}
          max={101}
          defaultValue={value}
          className={classes.slider}
          trackStyle={{ backgroundColor: sliderColor, height: 3 }}
          handleStyle={{
            borderColor: sliderColor,
            cursor: 'auto'
          }}
          railStyle={{ backgroundColor: 'transparent' }}
        />
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(ExaminationProgress);