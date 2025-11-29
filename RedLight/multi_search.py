"""
Multi-Site Search - Search across all supported sites simultaneously.
"""

import concurrent.futures
from typing import List, Dict, Optional, Callable, Any
from .sites import SiteRegistry


class MultiSiteSearch:
    """
    Search across all registered sites concurrently.
    
    Aggregates results from all supported sites and provides unified interface.
    """
    
    def __init__(self):
        self.registry = SiteRegistry()
    
    def search_all(
        self,
        query: str,
        page: int = 1,
        sort_by: str = "relevance",
        duration: Optional[str] = None,
        on_site_complete: Optional[Callable[[str, int], None]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search all sites concurrently and aggregate results.
        
        Args:
            query: Search query
            page: Page number
            sort_by: Sort preference (best effort across sites)
            duration: Duration filter (best effort across sites)
            on_site_complete: Callback(site_name, result_count) when each site finishes
        
        Returns:
            List of video results from all sites, with 'site' field indicating source
        """
        all_searchers = self.registry.get_all_searchers()
        all_results = []
        
        # Search each site in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(all_searchers)) as executor:
            # Submit all search tasks
            future_to_site = {
                executor.submit(
                    self._search_single_site,
                    searcher,
                    query,
                    page,
                    sort_by,
                    duration
                ): site_name
                for site_name, searcher in all_searchers.items()
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_site):
                site_name = future_to_site[future]
                try:
                    results = future.result()
                    all_results.extend(results)
                    
                    if on_site_complete:
                        on_site_complete(site_name, len(results))
                except Exception:
                    # Site search failed, skip it
                    if on_site_complete:
                        on_site_complete(site_name, 0)
        
        return all_results
    
    def _search_single_site(
        self,
        searcher,
        query: str,
        page: int,
        sort_by: str,
        duration: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Search a single site."""
        try:
            # Map common sort options to site-specific ones
            site_sort = sort_by
            if sort_by == "views" and "mostviewed" in searcher.get_search_filters().get("sort_by", []):
                site_sort = "mostviewed"
            
            return searcher.search(
                query=query,
                page=page,
                sort_by=site_sort,
                duration=duration
            )
        except Exception:
            return []
    
    def get_supported_sites(self) -> List[str]:
        """Get list of all supported site names."""
        sites = self.registry.get_all_sites()
        return [site["name"] for site in sites]
