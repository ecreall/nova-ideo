import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import NavigateNextIcon from '@material-ui/icons/NavigateNext';
import NavigateBeforeIcon from '@material-ui/icons/NavigateBefore';
import Fab from '@material-ui/core/Fab';

const styles = (theme) => {
  return {
    root: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      marginBottom: 15,
      marginTop: 15
    },
    controlContainer: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      width: '100%'
    },
    control: {
      width: 30,
      height: 30,
      minHeight: 30,
      marginLeft: 5,
      marginRight: 5,
      boxShadow: '0 1px 2px 0 rgba(0,0,0,.2)',
      backgroundColor: theme.palette.primary['500'],
      color: 'white',
      '&:hover': {
        opacity: 1
      }
    },
    sliderContainer: {
      marginLeft: 'auto',
      marginRight: 'auto'
    }
  };
};

export class DumbSlider extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentItem: props.current || 0
    };
  }

  onNextClick = () => {
    const { currentItem } = this.state;
    const { items } = this.props;
    let next = currentItem + 1;
    next = next >= items.length ? 0 : next;
    this.setState({ currentItem: next }, this.setColor);
  };

  onPreviousClick = () => {
    const { currentItem } = this.state;
    const { items } = this.props;
    let previous = currentItem - 1;
    previous = previous < 0 ? items.length - 1 : previous;
    this.setState({ currentItem: previous }, this.setColor);
  };

  render() {
    const { items, classes } = this.props;
    const { currentItem } = this.state;
    return (
      <div className={classes.root}>
        <div className={classes.sliderContainer}>{items[currentItem]}</div>
        {items.length > 1 ? (
          <div className={classes.controlContainer}>
            <Fab onClick={this.onPreviousClick} size="small" aria-label="previous" className={classes.control}>
              <NavigateBeforeIcon />
            </Fab>
            <Fab onClick={this.onNextClick} size="small" aria-label="next" className={classes.control}>
              <NavigateNextIcon />
            </Fab>
          </div>
        ) : null}
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbSlider);