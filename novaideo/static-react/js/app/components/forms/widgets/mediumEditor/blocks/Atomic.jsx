import React from 'react';
import { CircularProgress } from 'material-ui/Progress';

import BlockDataManager from '../BlockDataManager';

export class AtomicEmbedComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showIframe: false
    };
  }

  componentDidMount() {
    this.renderEmbedly();
  }

  componentDidUpdate(prevProps, prevState) {
    if (prevState.showIframe !== this.state.showIframe && this.state.showIframe === true) {
      this.renderEmbedly();
    }
  }

  getScript = () => {
    const script = document.createElement('script');
    script.async = 1;
    script.src = '//cdn.embedly.com/widgets/platform.js';
    script.onload = () => {
      window.embedly();
    };
    document.body.appendChild(script);
  };

  renderEmbedly = () => {
    if (window.embedly) {
      window.embedly();
    } else {
      this.getScript();
    }
  };

  render() {
    const { url } = this.props.data;
    return (
      <BlockDataManager {...this.props} className="md-block-with-data md-block-atomic-embed">
        <div className="embedly-card-url-container">
          <a className="embedly-card-url embedly-card" href={url} data-card-controls="0">
            <CircularProgress size={30} />
          </a>
        </div>
      </BlockDataManager>
    );
  }
}

export const AtomicSeparatorComponent = () => {
  return (
    <div className="md-block-atomic md-block-atomic-break">
      <hr className="text-node-separator" />
    </div>
  );
};

export const AtomicBlock = (props) => {
  const { blockProps, block, contentState } = props;
  const index = block.getEntityAt(0);
  let entitydata = null;
  let entityType = null;
  let entity = null;
  if (index !== null) {
    entity = contentState.getEntity(index);
    entitydata = entity.getData();
    entityType = entity.getType();
  }
  const data = block.getData();
  const position = data.get('position');
  const size = data.get('size');
  const type = data.get('type') || entityType;
  if (blockProps.components[type]) {
    const AtComponent = blockProps.components[type];
    return (
      <div className={`md-block-atomic-wrapper md-block-atomic-wrapper-${type}`}>
        <AtComponent
          {...props}
          readOnly={blockProps.readOnly}
          entity={index}
          data={{ ...entitydata, type: type, position: position, size: size }}
        />
      </div>
    );
  }
  return null;
};