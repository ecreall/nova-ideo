// @flow
import React from 'react';
import { withStyles } from 'material-ui/styles';
import PlayIcon from 'material-ui-icons/PlayCircleOutline';
import CloseIcon from 'material-ui-icons/Close';
import IconButton from 'material-ui/IconButton';

const styles = {
  container: {
    height: '100%'
  },
  sketchfabEmbed: {
    transitionProperty: 'background-color',
    transitionDuration: '2s',
    height: '100%'
  },
  sketchfabThumbnail: {
    position: 'relative',
    marginTop: 5,
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center center',
    backgroundSize: 'contain',
    borderRadius: 4,
    backgroundColor: 'black',
    boxShadow: '0 0 0 1px rgba(0, 0, 0, 0.1) inset',
    width: 360,
    height: 270,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden'
  },
  playButtonContainer: {
    minWidth: 150,
    maxWidth: 225,
    width: '100%',
    padding: '5%',
    borderRadius: 10,
    background: 'rgba(0, 0, 0, 0.4)',
    textAlign: 'center'
  },
  playButton: {
    opacity: 0.8,
    width: 60,
    height: 60,
    '&:hover': {
      opacity: 1
    }
  },
  playButtonIcon: {
    pointerEvents: 'none',
    color: 'white',
    width: 60,
    height: 60
  },
  closeEmbedButton: {
    color: '#545454',
    position: 'absolute',
    backgroundColor: 'white',
    boxShadow: '0 0px 7px rgba(0, 0, 0, 0.6)',
    top: 0,
    right: 0,
    margin: 15
  },
  sketchfabEmbedOpen: {
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    zIndex: 2000,
    position: 'fixed',
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
  },
  frame: {
    maxWidth: '100%'
  }
};

export class DumbSketchfabEmbed extends React.Component {
  state: {
    open: boolean
  };

  state = {
    open: false
  };

  closeEmbed = () => {
    return this.setState({ open: false });
  };

  openEmbed = () => {
    return this.setState({ open: true });
  };

  render = () => {
    const { id, imageUrl, classes } = this.props;
    const { open } = this.state;
    return (
      <div className={classes.container}>
        <div className={classes.sketchfabEmbed}>
          <div className={classes.sketchfabThumbnail} style={{ backgroundImage: `url(${imageUrl})` }}>
            <div className={classes.playButtonContainer}>
              <IconButton className={classes.playButton} onClick={this.openEmbed}>
                <PlayIcon className={classes.playButtonIcon} />
              </IconButton>
            </div>
          </div>
        </div>
        {open &&
          <div className={classes.sketchfabEmbedOpen} onClick={this.closeEmbed}>
            <iframe
              title="Sketchfab"
              id="SketchfabPlayer"
              type="text/html"
              width="640"
              height="360"
              className={classes.frame}
              src={`https://sketchfab.com/models/${id}/embed?autostart=1&autospin=0.5`}
              frameBorder="0"
            />
            <IconButton className={classes.closeEmbedButton} color="primary" onClick={this.closeEmbed}>
              <CloseIcon />
            </IconButton>
          </div>}
      </div>
    );
  };
}

export default withStyles(styles)(DumbSketchfabEmbed);