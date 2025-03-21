/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { inject, TestBed } from '@angular/core/testing';

import { EventManager, EventWithContent } from './event-manager.service';

describe('Event Manager tests', () => {
  describe('EventWithContent', () => {
    it('should create correctly EventWithContent', () => {
      // WHEN
      const eventWithContent = new EventWithContent('name', 'content');

      // THEN
      expect(eventWithContent).toEqual({ name: 'name', content: 'content' });
    });
  });

  describe('EventManager', () => {
    let recievedEvent: EventWithContent<unknown> | string | null;

    beforeEach(() => {
      TestBed.configureTestingModule({
        providers: [EventManager],
      });
      recievedEvent = null;
    });

    it('should not fail when nosubscriber and broadcasting', inject([EventManager], (eventManager: EventManager) => {
      expect(eventManager.observer).toBeUndefined();
      eventManager.broadcast({ name: 'modifier', content: 'modified something' });
    }));

    it('should create an observable and callback when broadcasted EventWithContent', inject(
      [EventManager],
      (eventManager: EventManager) => {
        // GIVEN
        eventManager.subscribe('modifier', (event: EventWithContent<unknown> | string) => (recievedEvent = event));

        // WHEN
        eventManager.broadcast({ name: 'unrelatedModifier', content: 'unreleated modification' });
        // THEN
        expect(recievedEvent).toBeNull();

        // WHEN
        eventManager.broadcast({ name: 'modifier', content: 'modified something' });
        // THEN
        expect(recievedEvent).toEqual({ name: 'modifier', content: 'modified something' });
      }
    ));

    it('should create an observable and callback when broadcasted string', inject([EventManager], (eventManager: EventManager) => {
      // GIVEN
      eventManager.subscribe('modifier', (event: EventWithContent<unknown> | string) => (recievedEvent = event));

      // WHEN
      eventManager.broadcast('unrelatedModifier');
      // THEN
      expect(recievedEvent).toBeNull();

      // WHEN
      eventManager.broadcast('modifier');
      // THEN
      expect(recievedEvent).toEqual('modifier');
    }));

    it('should subscribe to multiple events', inject([EventManager], (eventManager: EventManager) => {
      // GIVEN
      eventManager.subscribe(['modifier', 'modifier2'], (event: EventWithContent<unknown> | string) => (recievedEvent = event));

      // WHEN
      eventManager.broadcast('unrelatedModifier');
      // THEN
      expect(recievedEvent).toBeNull();

      // WHEN
      eventManager.broadcast({ name: 'modifier', content: 'modified something' });
      // THEN
      expect(recievedEvent).toEqual({ name: 'modifier', content: 'modified something' });

      // WHEN
      eventManager.broadcast('modifier2');
      // THEN
      expect(recievedEvent).toEqual('modifier2');
    }));
  });
});
