/* eslint-disable react/no-array-index-key, no-confusing-arrow */
/* eslint-disable no-param-reassign */
import React from 'react';
import { I18n } from 'react-redux-i18n';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  container: {
    display: 'inline',
    justifyContent: 'space-around',
    width: '100%',
    alignItems: 'center'
  },
  label: {
    fontWeight: 'bold',
    margin: '0 0 10px',
    display: 'block',
    fontSize: 17
  },
  labelOptional: {
    fontWeight: '400 !important',
    color: '#717274 !important'
  },
  itemContainer: {
    borderRadius: 5,
    cursor: 'pointer',
    boxShadow: '0 1px 1px rgba(0,0,0,.2)',
    margin: '0 10px 10px',
    display: 'inline-flex'
  },
  selectedItemContainer: {
    border: 'solid 3px #2e7d32',
    boxShadow: '0px 2px 4px -1px rgba(0,0,0,0.2), 0px 4px 5px 0px rgba(0,0,0,0.14), 0px 1px 10px 0px rgba(0,0,0,0.12)'
  }
};

export class DumbSelect extends React.Component {
  constructor(props) {
    super(props);
    const { options, value } = this.props;
    this.state = {
      options: options,
      selected: value
    };
  }

  componentDidMount() {
    const { initRef } = this.props;
    if (initRef) {
      initRef(this);
    }
  }

  toggleOption = (id) => {
    const { selected } = this.state;
    const { onChange } = this.props;
    const newValue = selected === id ? null : id;
    this.setState(
      {
        selected: newValue
      },
      () => {
        return onChange(newValue);
      }
    );
  };

  render = () => {
    const {
      name, label, optional, classes
    } = this.props;
    const { options, selected } = this.state;
    return (
      <div className={classes.container} role="menu">
        {label && (
          <label className={classes.label} htmlFor={name}>
            {label}
            {optional && (
              <span className={classes.labelOptional}>
                {' '}
                {I18n.t('forms.optional')}
              </span>
            )}
          </label>
        )}
        {Object.keys(options).map((id) => {
          const title = options[id];
          const checked = selected === id;
          return (
            <div
              className={classNames(classes.itemContainer, { [classes.selectedItemContainer]: checked })}
              onClick={() => {
                this.toggleOption(id);
              }}
            >
              {title}
            </div>
          );
        })}
      </div>
    );
  };
}

export default withStyles(styles, { withTheme: true })(DumbSelect);