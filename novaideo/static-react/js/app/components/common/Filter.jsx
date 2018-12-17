import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Divider from '@material-ui/core/Divider';
import { connect } from 'react-redux';

import { getFormId } from '../../utils/globalFunctions';

const styles = (theme) => {
  return {
    root: {
      width: '100%'
    },
    heading: {
      fontSize: theme.typography.pxToRem(15)
    },
    secondaryHeading: {
      fontSize: theme.typography.pxToRem(15),
      color: theme.palette.text.secondary
    },
    icon: {
      verticalAlign: 'bottom',
      height: 20,
      width: 20
    },
    details: {
      alignItems: 'center'
    },
    column: {
      flexBasis: '33.33%'
    },
    helper: {
      borderLeft: `2px solid ${theme.palette.divider}`,
      padding: `${theme.spacing.unit}px ${theme.spacing.unit * 2}px`
    },
    link: {
      color: theme.palette.primary.main,
      textDecoration: 'none',
      '&:hover': {
        textDecoration: 'underline'
      }
    },
    expRoot: {
      display: 'none'
    },
    paper: {
      backgroundColor: '#f3f3f3'
    }
  };
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