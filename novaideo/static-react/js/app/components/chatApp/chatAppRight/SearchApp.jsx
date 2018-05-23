import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import RightContent from './RightContent';
import Search from './Search';

const styles = {
  appTitle: {
    display: 'flex',
    alignItems: 'center'
  }
};

const SearchApp = (props) => {
  const { classes } = props;
  return (
    <RightContent
      title={
        <div className={classes.appTitle}>
          <span>
            {I18n.t('channels.searchBlockTitle')}
          </span>
        </div>
      }
    >
      <Search {...props} />
    </RightContent>
  );
};

export default withStyles(styles)(SearchApp);