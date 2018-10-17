/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

const styles = (theme) => {
  return {
    heading: {
      fontWeight: 900,
      fontSize: 20
    },
    secondaryHeading: {
      fontSize: 14,
      color: theme.palette.text.secondary
    },
    panelRoot: {
      boxShadow: 'none !important',
      '&:first-child': {
        borderTopLeftRadius: 6,
        borderTopRightRadius: 6
      },
      '&:last-child': {
        borderBottomLeftRadius: 6,
        borderBottomRightRadius: 6
      }
    },
    panelExpanded: {
      borderRadius: 6
    },
    summaryRoot: {
      display: 'block',
      opacity: '1 !important'
    },
    summaryContainer: {
      display: 'flex'
    },
    summaryContent: {
      margin: '0 !important'
    },
    detailsContainer: {
      width: '100%'
    },
    summaryIcon: {
      padding: 10,
      backgroundColor: theme.palette.info[500],
      color: 'white',
      borderRadius: 6,
      marginRight: 10,
      height: 24,
      width: 24
    },
    panelDisabled: {
      backgroundColor: 'transparent !important'
    }
  };
};

export const DumbTab = ({
  disabled, title, description, Icon, content, color, onChange, expanded, classes
}) => {
  return (
    <ExpansionPanel
      disabled={disabled}
      expanded={expanded}
      onChange={onChange}
      classes={{
        root: classes.panelRoot,
        expanded: classes.panelExpanded,
        disabled: disabled && classes.panelDisabled
      }}
    >
      <ExpansionPanelSummary
        classes={{
          root: classes.summaryRoot,
          content: classes.summaryContent
        }}
        expandIcon={!disabled && <ExpandMoreIcon />}
      >
        <p className={classes.summaryContainer}>
          {Icon && (
            <div style={color ? { backgroundColor: color } : {}} className={classes.summaryIcon}>
              <Icon />
            </div>
          )}
          <div>
            <Typography className={classes.heading}>{title}</Typography>
            <Typography className={classes.secondaryHeading}>{description}</Typography>
          </div>
        </p>
      </ExpansionPanelSummary>
      <ExpansionPanelDetails>
        <Typography className={classes.detailsContainer}>{content}</Typography>
      </ExpansionPanelDetails>
    </ExpansionPanel>
  );
};

export default withStyles(styles, { withTheme: true })(DumbTab);