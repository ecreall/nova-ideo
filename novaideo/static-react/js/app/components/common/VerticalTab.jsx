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
      boxShadow: '0px 1px 3px 0px rgba(0, 0, 0, 0.2), 0px 1px 1px 0px rgba(0, 0, 0, 0.14), 0px 2px 1px -3px rgba(0, 0, 0, 0.12)',
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
      display: 'block'
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
    }
  };
};

export class DumbVerticalTab extends React.Component {
  state = {
    expanded: -1
  };

  handleChange = (index) => {
    const { expanded } = this.state;
    this.setState({ expanded: expanded === index ? -1 : index });
  };

  renserEntry = (entry, index) => {
    const { classes } = this.props;
    const { expanded } = this.state;
    const { title, description, Icon, content, color } = entry;
    return (
      <ExpansionPanel
        expanded={expanded === index}
        onChange={() => {
          this.handleChange(index);
        }}
        classes={{
          root: classes.panelRoot,
          expanded: classes.panelExpanded,
          disabled: classes.panelDisabled
        }}
      >
        <ExpansionPanelSummary
          classes={{
            root: classes.summaryRoot,
            content: classes.summaryContent
          }}
          expandIcon={<ExpandMoreIcon />}
        >
          <p className={classes.summaryContainer}>
            {Icon &&
              <div style={color ? { backgroundColor: color } : {}} className={classes.summaryIcon}>
                <Icon />
              </div>}
            <div>
              <Typography className={classes.heading}>
                {title}
              </Typography>
              <Typography className={classes.secondaryHeading}>
                {description}
              </Typography>
            </div>
          </p>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails>
          <Typography className={classes.detailsContainer}>
            {content}
          </Typography>
        </ExpansionPanelDetails>
      </ExpansionPanel>
    );
  };

  render() {
    const { tabs, classes } = this.props;
    if (!tabs || tabs.length === 0) return null;
    return (
      <div className={classes.tabContainer}>
        {tabs.map((entry, index) => {
          return this.renserEntry(entry, index);
        })}
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbVerticalTab);