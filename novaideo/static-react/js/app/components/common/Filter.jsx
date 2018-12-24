import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Divider from '@material-ui/core/Divider';
import { connect } from 'react-redux';

import { getFormId } from '../../utils/globalFunctions';

const styles = {
  root: {
    width: '100%'
  },
  details: {
    alignItems: 'center'
  },
  paper: {
    backgroundColor: '#f3f3f3'
  }
};

function Filter(props) {
  const {
    id, filterOpened, closeFilterSection, Form, classes, ...restProps
  } = props;
  const formId = getFormId(`${id}-filter`);
  return (
    <div className={classes.root}>
      <ExpansionPanel classes={{ root: classes.paper }} expanded={filterOpened}>
        <ExpansionPanelDetails className={classes.details}>
          <Form id={id} form={formId} key={formId} {...restProps} />
        </ExpansionPanelDetails>
        <Divider />
      </ExpansionPanel>
    </div>
  );
}

export const mapStateToProps = (state, props) => {
  return {
    filterOpened: !!state.filter[props.id]
  };
};

export default withStyles(styles)(connect(mapStateToProps)(Filter));