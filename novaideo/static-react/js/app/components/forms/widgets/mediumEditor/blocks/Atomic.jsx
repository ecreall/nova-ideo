import React from 'react';
// import CircularProgress from '@material-ui/core/CircularProgress';

import BlockDataManager from '../BlockDataManager';
import URLMetadataLoader from '../../../../common/urlPreview/URLMetadataLoader';

export class AtomicEmbedComponent extends React.Component {
  render() {
    const { url } = this.props.data;
    return (
      <BlockDataManager {...this.props} className="md-block-with-data md-block-atomic-embed">
        <URLMetadataLoader url={url} />
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
          data={{
            ...entitydata, type: type, position: position, size: size
          }}
        />
      </div>
    );
  }
  return null;
};