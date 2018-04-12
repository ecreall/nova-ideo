/* eslint-disable react/no-array-index-key */
import React from 'react';
import Mousetrap from 'mousetrap';
import 'mousetrap/plugins/global-bind/mousetrap-global-bind';

export const keymap = {
  APP: {
    OPEN_USER_MENU: 'ctrl+m',
    APP_OPEN_JUMP: 'ctrl+Maj+k'
  },
  CHATAPP: {
    CHATAPP_OPEN_JUMP: 'ctrl+k',
    CHATAPP_CLOSE: 'ctrl+q',
    CHATAPP_INFO: 'ctrl+i'
  }
};

class ShortcutsManager extends React.Component {
  constructor(props) {
    super(props);
    this.mousetrapBindings = [];
  }

  componentDidMount() {
    const { shortcuts, domain } = this.props;
    const domainShortcuts = keymap[domain];
    if (domainShortcuts) {
      Object.keys(shortcuts).forEach((action) => {
        const keys = domainShortcuts[action];
        if (keys.length > 0) {
          this.bindShortcut(keys, shortcuts[action]);
        }
      });
    }
  }

  componentWillUnmount() {
    this.unbindAllShortcuts();
  }

  bindShortcut = (key, callback) => {
    Mousetrap.bindGlobal(key, callback);
    this.mousetrapBindings.push(key);
  };

  unbindShortcut = (key) => {
    const index = this.mousetrapBindings.indexOf(key);
    if (index > -1) {
      this.mousetrapBindings.splice(index, 1);
    }
    Mousetrap.unbind(key);
  };

  unbindAllShortcuts = () => {
    if (this.mousetrapBindings.length < 1) {
      return;
    }

    this.mousetrapBindings.forEach((binding) => {
      Mousetrap.unbind(binding);
    });
    this.mousetrapBindings = [];
  };

  render() {
    return this.props.children;
  }
}

export default ShortcutsManager;