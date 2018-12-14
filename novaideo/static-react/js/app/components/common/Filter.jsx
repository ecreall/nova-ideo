import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelActions from '@material-ui/core/ExpansionPanelActions';
import Button from '@material-ui/core/Button';
import Divider from '@material-ui/core/Divider';
import { connect } from 'react-redux';

import { clearFilter } from '../../actions/collaborationAppActions';

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
    }
  };
};

function Filter(props) {
  const {
    live, id, filter, closeFilterSection, Form, classes
  } = props;
  return (
    <div className={classes.root}>
      <ExpansionPanel expanded={!!filter}>
        <ExpansionPanelDetails className={classes.details}>
          <Form id={id} form={id} key={id} live={live} />
        </ExpansionPanelDetails>
        <Divider />
        <ExpansionPanelActions>
          <Button
            onClick={() => {
              closeFilterSection(id);
            }}
            size="small"
          >
            Close
          </Button>
        </ExpansionPanelActions>
      </ExpansionPanel>
    </div>
  );
}

export const mapStateToProps = (state, props) => {
  return {
    filter: state.filter[props.id]
  };
};

export const mapDispatchToProps = {
  closeFilterSection: clearFilter
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(Filter));