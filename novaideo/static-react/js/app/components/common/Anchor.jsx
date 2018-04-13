/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import Zoom from 'material-ui/transitions/Zoom';

const styles = {
  container: {
    transform: 'scale(0)'
  }
};

export class DumbAnchor extends React.Component {
  state = {
    visible: true
  };

  componentDidMount() {
    const { scrollEvent } = this.props;
    document.addEventListener(scrollEvent, this.handleScroll);
    setTimeout(this.initVisibility, 100);
  }

  componentWillUnmount() {
    const { scrollEvent } = this.props;
    document.removeEventListener(scrollEvent, this.handleScroll);
  }

  updateVisibility = (clientHeight, scrollTop) => {
    const { visible } = this.state;
    const { getAnchor } = this.props;
    const anchor = getAnchor();
    const isTop = scrollTop <= anchor.offsetTop;
    const anchorVisible = isTop ? anchor.offsetTop - clientHeight <= scrollTop : anchor.offsetTop + clientHeight >= scrollTop;
    if (visible !== anchorVisible) this.setState({ visible: anchorVisible });
  };

  handleScroll = (event) => {
    const { clientHeight, scrollTop } = event.values;
    this.updateVisibility(clientHeight, scrollTop);
  };

  initVisibility = () => {
    const { getAnchor } = this.props;
    const anchor = getAnchor();
    if (anchor) {
      const parent = anchor.offsetParent;
      this.updateVisibility(parent.clientHeight, parent.scrollTop);
    }
  };

  scrollToAnchor = () => {
    const { getAnchor } = this.props;
    const anchor = getAnchor();
    const parent = anchor.offsetParent;
    const top = anchor.offsetTop - parent.clientHeight / 2;
    parent.scrollTo({ top: top >= 0 ? top : 0, left: 0, behavior: 'smooth' });
  };

  render() {
    const { children, classes } = this.props;
    const { visible } = this.state;
    return (
      <Zoom in={!visible} timeout={100}>
        <div className={classes.container} onClick={this.scrollToAnchor}>
          {children}
        </div>
      </Zoom>
    );
  }
}

export default withStyles(styles)(DumbAnchor);