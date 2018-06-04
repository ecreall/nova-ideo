/* eslint-disable react/no-array-index-key, no-confusing-arrow */
/* eslint-disable no-param-reassign */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  container: {
    width: '100%',
    marginBottom: 10
  },
  label: {
    fontWeight: 'bold',
    margin: '0 0 .25rem',
    display: 'block',
    fontSize: 17
  },
  selectContainer: {
    position: 'relative',
    '&::after': {
      content: '"\\F35D"',
      color: '#2c2d30',
      font: 'normal normal normal 24px/1 "Material Design Icons"',
      position: 'absolute',
      right: 13,
      bottom: 10,
      fontSize: 29,
      pointerEvents: 'none',
      '&:hover': {
        color: 'gray'
      }
    }
  },
  select: {
    fontSize: 16,
    lineHeight: 'normal',
    padding: 13.5,
    paddingRight: 35,
    border: '1px solid #919193',
    borderRadius: 3,
    appearance: 'none',
    outline: 0,
    color: '#2c2d30',
    width: '100%',
    maxWidth: '100%',
    margin: '0 0 3px',
    marginTop: 0,
    marginBottom: 3,
    fontVariantLigatures: 'none',
    transition: 'box-shadow 70ms ease-out,border-color 70ms ease-out',
    boxShadow: 'none',
    height: 'auto',
    background: 'white'
  }
};

export class DumbSelectField extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      options: props.options,
      selected: props.value
    };
  }

  componentDidMount() {
    if (this.props.initRef) {
      this.props.initRef(this);
    }
  }

  toggleOption = (event) => {
    const value = event.target.value;
    this.setState(
      {
        selected: value
      },
      () => {
        return this.props.onChange(value);
      }
    );
  };

  render() {
    const { name, classes } = this.props;
    const { options, selected } = this.state;
    return (
      <div className={classes.container}>
        {this.props.label && (
          <label className={classes.label} htmlFor={name}>
            {this.props.label}
          </label>
        )}
        <div className={classes.selectContainer}>
          <select
            className={classes.select}
            name={name}
            onChange={(value) => {
              this.toggleOption(value);
            }}
          >
            {Object.keys(options).map((id) => {
              const title = options[id];
              return (
                <option key={id} value={id} selected={id === selected}>
                  {title}
                </option>
              );
            })}
          </select>
        </div>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbSelectField);