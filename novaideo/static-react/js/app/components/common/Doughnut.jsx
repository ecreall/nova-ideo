import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { Translate } from 'react-redux-i18n';

import Tooltip from './overlay/Tooltip';
import Doughnut from '../svg/doughnut';

const styles = {
  statisticsDoughnut: {
    textAlign: 'center',
    display: 'inline-block',
    height: 100,
    marginTop: 30,
    marginBottom: 30,
    minWidth: 120,
    padding: '0 0 0',
    right: 0,
    width: '20%',
    '& .circle': {
      strokeWidth: 11,
      fill: 'transparent'
    }
  },
  statistics: {
    position: 'relative',
    width: '100%',
    height: '100%',
    display: 'flex',
    flexDirection: 'column'
  },
  superpose: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    '& svg': {
      width: '100%',
      height: '100%'
    }
  },
  labelSuperpose: {
    position: 'absolute',
    top: '48%',
    left: '50%',
    transform: 'translateX(-50%) translateY(-50%)',
    width: 'auto',
    height: 'auto'
  },
  after: {},
  doughnutLabelCount: {
    fontSize: 16,
    letterSpacing: 'initial',
    fontWeight: 900
  },
  doughnutLabelText: {
    fontFamily: 'LatoWebLight',
    fontSize: 10,
    letterSpacing: 'initial'
  },
  caption: {
    fontFamily: 'LatoWebLight',
    fontSize: 10,
    letterSpacing: 'initial',
    marginTop: -5
  }
};

export const createTooltip = (title, count, className) => {
  return (
    <Tooltip className={className}>
      {count} {title}
    </Tooltip>
  );
};

const StatisticsDoughnut = ({ elements, placement, title, caption, disableTotalCount, classes }) => {
  const totalCount = elements.reduce((result, element) => {
    return result + element.count;
  }, 0);
  const placeAfter = placement === 'after';
  return (
    <div className={classes.statisticsDoughnut}>
      <div className={classes.statistics}>
        <div className={!placeAfter && classes.superpose}>
          <Doughnut elements={elements} />
        </div>
        {!disableTotalCount && (
          <div className={placeAfter ? classes.after : classes.labelSuperpose}>
            <div className={classes.doughnutLabelCount}>{totalCount}</div>
            {placeAfter ? ' ' : ''}
            {title && (
              <div className={classes.doughnutLabelText}>
                <Translate value={title} count={totalCount} />
              </div>
            )}
          </div>
        )}
      </div>
      {caption && (
        <div className={classes.caption}>
          <Translate value={caption} count={totalCount} />
        </div>
      )}
    </div>
  );
};

export default withStyles(styles)(StatisticsDoughnut);