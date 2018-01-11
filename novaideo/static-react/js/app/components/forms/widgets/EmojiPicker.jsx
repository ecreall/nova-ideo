import React from 'react';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';
import { Picker } from 'emoji-mart';
import InsertEmoticonIcon from 'material-ui-icons/InsertEmoticon';

const styles = {
  picker: {
    boxShadow: '0 5px 10px rgba(0,0,0,.12)',
    fontFamily: '"LatoWebMedium", "Helvetica Neue", Helvetica, Arial, sans-serif',
    position: 'absolute',
    right: -35,
    bottom: 36
  }
};

const classesStyles = (theme) => {
  return {
    button: {
      display: 'flex',
      color: 'gray',
      cursor: 'pointer'
    },
    buttonActive: {
      color: theme.palette.primary[500]
    }
  };
};

class EmojiPicker extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      opened: false
    };
    this.picker = null;
    this.button = null;
  }

  componentDidMount() {
    document.addEventListener('click', this.closePicker);
  }

  componentWillUnmount() {
    document.removeEventListener('click', this.closePicker);
  }

  openPicker = () => {
    this.setState({ opened: true });
  };

  closePicker = (event) => {
    if (this.state.opened && this.picker && !this.picker.contains(event.target) && !this.button.contains(event.target)) {
      this.setState({ opened: false });
    }
  };

  onEmojiSelect = (emoji) => {
    const { onSelect } = this.props;
    if (onSelect) {
      this.setState({ opened: false });
      onSelect(emoji.colons);
    }
  };

  render() {
    const { theme, classes } = this.props;
    const items = [
      <div
        className={classNames(classes.button, {
          [classes.buttonActive]: this.state.opened
        })}
        ref={(button) => {
          this.button = button;
        }}
      >
        <InsertEmoticonIcon onClick={this.openPicker} />
      </div>
    ];
    if (this.state.opened) {
      items.push(
        <div
          ref={(picker) => {
            this.picker = picker;
          }}
        >
          <Picker
            color={theme.palette.primary[500]}
            title="Emoji"
            emoji="slightly_smiling_face"
            sheetSize={32}
            style={styles.picker}
            onClick={this.onEmojiSelect}
          />
        </div>
      );
    }

    return items;
  }
}

export default withStyles(classesStyles, { withTheme: true })(EmojiPicker);