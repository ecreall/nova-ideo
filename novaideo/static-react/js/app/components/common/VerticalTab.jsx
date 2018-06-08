/* eslint-disable react/no-array-index-key */
import React from 'react';

import Tab from './Tab';

export class DumbVerticalTab extends React.Component {
  constructor(props) {
    super(props);
    this.uniqueTab =
      props.tabs.filter((tab) => {
        return !tab.invalidate;
      }).length === 1;
    this.state = {
      expanded:
        props.tabs.length > 1
          ? props.tabs.findIndex((tab) => {
            return tab.open;
          })
          : 0
    };
  }

  handleChange = (index) => {
    const { expanded } = this.state;
    this.setState({ expanded: expanded === index ? -1 : index });
  };

  renderEntry = (entry, index) => {
    if (!entry || entry.invalidate) return null;
    const { expanded } = this.state;
    return (
      <Tab
        {...entry}
        disabled={this.uniqueTab}
        expanded={expanded === index}
        onChange={() => {
          this.handleChange(index);
        }}
      />
    );
  };

  render() {
    const { tabs, classes } = this.props;
    if (!tabs || tabs.length === 0) return null;
    return (
      <div className={classes.tabContainer}>
        {tabs.map((entry, index) => {
          return this.renderEntry(entry, index);
        })}
      </div>
    );
  }
}

export default DumbVerticalTab;