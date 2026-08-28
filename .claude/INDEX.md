# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (265)

```
 10745  GET              /                                                dashboard
 15849  GET              /api/abo/status                                  api_abo_status
 10853  GET              /api/active-recordings                           api_active_recordings
 15924  GET              /api/activity-pulse                              api_activity_pulse
 15277  GET              /api/ai-log                                      api_ai_log
 11331  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 15684  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 23834  GET/POST         /api/audio/config                                api_audio_config
 23864  POST             /api/audio/testtone                              api_audio_testtone
 15790  GET/POST         /api/auto-archive-rules                          api_archive_rules
 15814  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 15818  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12620  GET              /api/automation/status                           api_automation_status
 12642  POST             /api/automation/toggle                           api_automation_toggle
 14435  GET              /api/azrael/agents                               api_azrael_agents
 12512  POST             /api/azrael/ask                                  api_azrael_ask
 24070  GET/POST         /api/azrael/context                              api_azrael_context
 14062  GET              /api/azrael/core                                 api_azrael_core
 24204  POST             /api/azrael/live_pause                           api_azrael_live_pause
 24194  GET              /api/azrael/live_status                          api_azrael_live_status
 24212  POST             /api/azrael/live_test                            api_azrael_live_test
 14444  GET              /api/azrael/memories                             api_azrael_memories
 24260  POST             /api/azrael/persona                              api_azrael_persona_set
 24251  GET              /api/azrael/personas                             api_azrael_personas
 24288  GET              /api/azrael/piper_status                         api_azrael_piper_status
 24043  POST             /api/azrael/react                                api_azrael_react
 24079  GET              /api/azrael/reaction                             api_azrael_reaction
 24231  GET              /api/azrael/reactions                            api_azrael_reactions
 24281  GET              /api/azrael/transcript                           api_azrael_transcript
 24166  POST             /api/azrael/tts_test                             api_azrael_tts_test
 24141  GET              /api/azrael/voices                               api_azrael_voices
 24305  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11426  GET              /api/backoff-watch                               api_backoff_watch
 15048  POST             /api/backup/run                                  api_backup_run
 15014  GET              /api/backup/status                               api_backup_status
 15003  POST             /api/backup/system                               api_backup_system
 15756  GET              /api/bandwidth/live                              api_bandwidth_live
 15669  GET              /api/bookmarks                                   api_bookmarks_list
 11689  GET              /api/brain                                       api_brain
 11626  GET              /api/brain/alarms                                api_brain_alarms
 11611  GET              /api/brain/creator                               api_brain_creator
 11588  GET              /api/brain/graph                                 api_brain_graph
 11649  GET              /api/brain/growth                                api_brain_growth
 10299  GET              /api/brain/health                                api_brain_health
 24786  GET              /api/channel/categories                          api_channel_categories
 24792  POST             /api/channel/set                                 api_channel_set
 24602  GET              /api/channels/status                             api_channels_status
 23431  POST             /api/chat/send                                   api_chat_send
 14702  GET              /api/chat/send_status                            api_chat_send_status
 10834  GET              /api/checks                                      api_checks
 24107  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 24090  GET              /api/clips                                       api_clips
 24123  POST/DELETE      /api/clips/clear                                 api_clips_clear
 23709  GET              /api/cohost                                      api_cohost
 23721  POST             /api/cohost/config                               api_cohost_config
 16488  GET              /api/community/stats                             api_community_stats
 25786  POST             /api/config/restore                              api_config_restore
 25771  GET              /api/config/snapshot                             api_config_snapshot
 15947  GET              /api/cookies/age                                 api_cookies_age
 10901  GET              /api/cookies/health                              api_cookies_health
 10908  POST             /api/cookies/update                              api_cookies_update
 25737  GET              /api/data/export                                 api_data_export
 17100  GET              /api/db/export                                   api_db_export
 17127  POST             /api/db/import                                   api_db_import
 17087  GET              /api/db/summary                                  api_db_summary
 23635  GET              /api/debug/threads                               api_debug_threads
 26672  GET              /api/defense/attacks                             api_defense_attacks
 26639  GET              /api/defense/crowdsec                            api_defense_crowdsec
 26657  GET              /api/defense/fail2ban                            api_defense_fail2ban
 26363  GET              /api/defense/overview                            api_defense_overview
 15110  POST             /api/discord/announce                            api_discord_announce
 14838  GET              /api/discord/clips_week                          api_discord_clips_week
 15054  GET              /api/discord/community                           api_discord_community
 14730  GET              /api/discord/invite                              api_discord_invite
 14193  GET              /api/discord/overview                            api_discord_overview
 14279  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16565  POST             /api/donations/add                               api_donations_add
 16598  GET              /api/donations/manual                            api_donations_manual
 16606  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16501  POST             /api/donations/reset                             api_donations_reset
 16622  GET              /api/donations/summary                           api_donations_summary
 15738  GET              /api/events                                      api_events
 14885  GET              /api/events/stream                               api_events_stream
 17853  GET              /api/evolution/changelog                         api_evolution_changelog
 17838  GET              /api/evolution/history                           api_evolution_history
 17778  GET              /api/evolution/learned                           api_evolution_learned
 17800  GET              /api/evolution/proposals                         api_evolution_proposals
 17821  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17768  POST             /api/evolution/run                               api_evolution_run
 17868  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17733  GET              /api/evolution/status                            api_evolution_status
 16905  GET              /api/finanzamt/entries                           api_finanzamt_entries
 16925  POST             /api/finanzamt/entry                             api_finanzamt_add
 16952  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15751  GET              /api/forecast/storage                            api_forecast_storage
 12658  GET              /api/freeai/status                               api_freeai_status
 14135  GET              /api/health                                      api_health
 15769  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15765  GET              /api/heatmap/recordings                          api_heatmap_recordings
 23758  GET              /api/highlights                                  api_highlights
 23770  POST             /api/highlights/config                           api_highlights_config
 24643  GET              /api/kick/channel                                api_kick_channel
 24664  POST             /api/kick/channel                                api_kick_channel_set
 13862  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13930  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13908  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13847  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13887  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23882  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23951  POST             /api/kickmod/config                              api_kickmod_config
 23996  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 24010  GET              /api/kickmod/learned                             api_kickmod_learned
 24037  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 24017  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 24348  POST             /api/kickmod/say                                 api_kickmod_say
 24324  POST             /api/kickmod/start                               api_kickmod_start
 23922  GET              /api/kickmod/status                              api_kickmod_status
 24335  POST             /api/kickmod/stop                                api_kickmod_stop
 10679  POST             /api/login                                       dashboard_login_submit
 16473  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13073  POST             /api/marketing/config                            api_marketing_config
 13098  GET              /api/marketing/preview                           api_marketing_preview
 13108  POST             /api/marketing/send-now                          api_marketing_send_now
 13047  GET              /api/marketing/status                            api_marketing_status
 13065  POST             /api/marketing/toggle                            api_marketing_toggle
 23785  GET              /api/moderation/feed                             api_moderation_feed
 13626  POST             /api/news/config                                 api_news_config
 13592  GET              /api/news/creators                               api_news_creators
 13603  POST             /api/news/creators/generate                      api_news_creators_generate
 13668  POST             /api/news/generate-now                           api_news_generate_now
 13663  GET              /api/news/items                                  api_news_items
 13654  GET              /api/news/preview                                api_news_preview
 13573  GET              /api/news/status                                 api_news_status
 13618  POST             /api/news/toggle                                 api_news_toggle
 16330  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14667  GET              /api/notify/status                               api_notify_status
 14678  POST             /api/notify/test                                 api_notify_test
 14653  GET              /api/ops/audit                                   api_ops_audit
 16401  GET              /api/ops/db-stats                                api_ops_db_stats
 16429  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14459  GET              /api/ops/errors                                  api_ops_errors
 16350  GET              /api/ops/healthcheck                             api_ops_healthcheck
 17280  GET              /api/ops/log-tail                                api_ops_log_tail
 12492  GET              /api/ops/logtail                                 api_ops_logtail
 14400  GET              /api/ops/metrics                                 api_ops_metrics
 14383  GET              /api/ops/resource_history                        api_ops_resource_history
 17156  GET              /api/ops/version                                 api_ops_version
 11184  GET              /api/outcomes                                    api_outcomes
 25267  POST             /api/overlay/config                              api_overlay_config
 25254  POST             /api/overlay/event                               api_overlay_event
 25159  GET              /api/overlay/state                               api_overlay_state
 11217  GET              /api/profile/<username>                          api_profile
 15955  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15777  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15903  GET              /api/proxy/heatmap                               api_proxy_heatmap
 15880  GET              /api/proxy/trend                                 api_proxy_trend
 13547  GET              /api/public/stats                                api_public_stats
 10779  GET              /api/pulse                                       api_pulse
 15301  GET              /api/recording-attempts                          api_recording_attempts
 23366  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 23344  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 23385  POST             /api/restream/<int:rid>/start                    api_restream_start
 23656  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 25121  GET              /api/restream/chatfeed                           api_restream_chatfeed
 23320  POST             /api/restream/create                             api_restream_create
 13938  GET              /api/restream/deck                               api_restream_deck
 12594  GET              /api/restream/health                             api_restream_health
 25143  POST             /api/restream/layout                             api_restream_layout
 23293  GET              /api/restream/list                               api_restream_list
 12563  POST             /api/restream/report                             api_restream_report
 23669  POST             /api/restream/start_all                          api_restream_start_all
 23695  POST             /api/restream/stop_all                           api_restream_stop_all
 12821  GET              /api/restream/testpush                           api_testpush_status
 12846  POST             /api/restream/testpush                           api_testpush_run
 16738  GET              /api/restream/verify                             api_restream_verify
 14816  GET              /api/retention/preview                           api_retention_preview
 14825  POST             /api/retention/run                               api_retention_run
 25852  POST             /api/schedule/add                                api_schedule_add
 25842  GET              /api/schedule/list                               api_schedule_list
 25877  POST             /api/schedule/remove                             api_schedule_remove
 15654  GET              /api/search                                      api_search
 26410  GET              /api/selftest                                    api_selftest
 23402  GET              /api/shield/stats                                api_shield_stats
 10798  GET              /api/stats                                       api_stats
 15918  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 15845  GET              /api/stats/tiktok-status                         api_tiktok_status
 25817  GET              /api/stats/timeline                              api_stats_timeline
 10875  GET              /api/storage                                     api_storage
 10882  POST             /api/storage/cleanup                             api_storage_cleanup
 15831  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12533  GET              /api/stream/timeline                             api_stream_timeline
 14267  GET              /api/stream/transcript                           api_stream_transcript
 25485  GET              /api/streamer/compare                            api_streamer_compare
 25684  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14777  GET              /api/streamer/detail                             api_streamer_detail
 25709  GET              /api/streamer/digest/<username>                  api_streamer_digest
 25589  GET              /api/streamer/dormant                            api_streamer_dormant
 25665  GET              /api/streamer/exists/<username>                  api_streamer_exists
 25544  GET              /api/streamer/journal/<username>                 api_streamer_journal
 25509  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 25569  GET              /api/streamer/watchlist                          api_streamer_watchlist
 14102  GET              /api/streamers/wall                              api_streamers_wall
 11024  GET              /api/summary/preview                             api_summary_preview
 15366  GET              /api/system                                      api_system
 16686  GET              /api/system/check_timing                         api_check_timing
 17068  GET              /api/system/config_drift                         api_config_drift
 14303  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14514  GET              /api/system/preflight                            api_system_preflight
 14640  GET              /api/system/preflight_history                    api_system_preflight_history
 14950  GET              /api/system/resilience                           api_system_resilience
 15689  GET              /api/tags                                        api_tags_list
 10848  GET              /api/top                                         api_top
 12466  GET              /api/trackings                                   api_trackings
 16219  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 16252  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15725  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 15938  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 16281  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15711  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 15140  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 15187  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 15216  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 15198  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 11110  POST             /api/trackings/bulk                              api_trackings_bulk
 15155  GET              /api/trackings/export                            api_trackings_export
 11079  GET              /api/trackings/groups                            api_trackings_groups
 15693  GET              /api/trackings/tags-map                          api_trackings_tags_map
 15993  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11481  GET              /api/trend-7d                                    api_trend_7d
 24155  GET              /api/tts/<fn>                                    api_tts_file
 12701  POST             /api/tunnel/set                                  api_tunnel_set
 12680  GET              /api/tunnel/status                               api_tunnel_status
 12712  POST             /api/tunnel/test                                 api_tunnel_test
 12693  POST             /api/tunnel/toggle                               api_tunnel_toggle
 17040  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 16992  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 17016  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 16970  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 17228  GET              /api/update/backups                              api_update_backups
 17194  GET              /api/update/check                                api_update_check
 17253  POST             /api/update/restart                              api_update_restart
 17233  POST             /api/update/rollback                             api_update_rollback
 17216  POST             /api/update/start                                api_update_start
 17209  GET              /api/update/status                               api_update_status
 25295  GET              /api/upload_window                               api_upload_window
 11198  GET              /api/userstats                                   api_userstats
 13679  GET              /api/version                                     api_version
 16832  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 16853  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 16865  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 16790  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 16814  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16768  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 30092  GET              /api/youtube/sendrate                            api_youtube_sendrate
 15339  GET              /archive/<int:eid>/download                      archive_download
 15396  GET              /download/<int:recording_id>                     download
 15262  GET              /health                                          health
 23604  GET              /healthz                                         healthz
 10670  GET              /login                                           dashboard_login_page
 10700  GET              /logout                                          dashboard_logout
 10707  GET              /manifest.webmanifest                            pwa_manifest
 14331  GET              /metrics                                         api_prometheus_metrics
 25104  GET              /overlay                                         overlay_page
 10731  GET              /pwa-icon-<variant>.png                          pwa_icon
 10717  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (90)

```
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   814  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   896  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   924  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   935  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   801  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   863  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   850  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   831  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   476  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   471  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   519  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   402  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   729  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   493  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   456  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   429  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   573  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   662  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   568  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   501  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   281  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   746  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   369  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   624  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   779  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   764  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   325  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   563  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   549  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   532  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   589  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   682  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   578  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 27115  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 27574  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 27206  /assign_role            Rolle/Gruppe einem Mitglied geben
 27252  /ban                    Mitglied bannen
 27906  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 27830  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 27870  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 27855  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 27697  /clips                  Letzte Highlight-Clips eines Users
 27167  /create_category        Kategorie anlegen
 27136  /create_channel         Text-Channel anlegen (optional in Kategorie)
 27195  /create_group           Nutzergruppe (= Rolle) anlegen
 27178  /create_role            Rolle / Nutzergruppe anlegen
 27152  /create_voice           Voice-Channel anlegen
 27488  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 27604  /event                  Community-Event ankündigen (Admin) — mit Countdown
 27647  /events                 Kommende Community-Events anzeigen
 27743  /follow                 Bei Live-Gang eines Streamers gepingt werden
 27727  /help                   Alle Bot-Befehle anzeigen
 27241  /kick                   Mitglied kicken
 27470  /leaderboard            Top-10 der Community nach XP
 27683  /livenow                Welche getrackten User sind gerade live
 27713  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 27544  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 27276  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 27456  /rank                   Dein Level und Rang anzeigen
 27670  /recstatus              Aktuell laufende Aufnahmen
 27217  /remove_role            Rolle/Gruppe entfernen
 27129  /restream_status        Restream-Status
 27228  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 27421  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 27439  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 27769  /stats                  Statistik zu einem getrackten Streamer
 27041  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 28065  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 27962  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 27938  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 27263  /timeout                Mitglied stummschalten (Minuten)
 27841  /topstreamers           Rangliste der Streamer nach Aufnahmen
 27071  /track                  TikTok-User tracken
 27055  /tracklist              Getrackte TikTok-User dieses Servers
 27758  /unfollow               Live-Pings für einen Streamer abbestellen
 27104  /untrack                TikTok-User nicht mehr tracken
 27791  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 27815  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 28549  on_member_join
 28511  on_message
 28152  on_raw_reaction_add
 28584  on_ready
```

## Top-Level-Symbole in bot.py (565 Funktionen, 2 Klassen)

```
  2469-2470   _abo_key
  2490-2508   _abo_probe_dump
 25952-25962  _active_recorder_sync
 20590-20597  _ad_allowlist
 21712-21718  _agent_for
 25964-25982  _ai_calls_total_sync
 21721-21737  _ai_telemetry
 22219-22237  _alert
 28697-28747  _alert_monitor_loop
 29123-29185  _announce_loop
  3411-3414   _anthropic_key
  3421-3423   _anthropic_model
 10427-10430  _arg_int
  2461-2466   _as_dict
 18450-18455  _audio_cfg
 22373-22395  _audio_tap_cmd
 10591-10602  _auth_cookie
 10558-10587  _auth_guard
  1617-1622   _auto_on
 23269-23287  _auto_restream_loop
 30253-30268  _azrael_broadcast_reply
 30153-30175  _azrael_chat_reply
 30136-30150  _azrael_chat_should_reply
 13273-13291  _azrael_creator_take
 30181-30183  _azrael_gate_cfg
 21742-21756  _azrael_live_state
 25003-25017  _azrael_overlay_state
 22102-22156  _azrael_proactive_loop
 21561-21617  _azrael_reaction_to_chats
 30186-30193  _azrael_reply_all_chats
 30123-30133  _azrael_self_names
 30221-30250  _azrael_send_to
 21759-21780  _azrael_system
 28863-28866  _backup_active
 28944-28957  _backup_loop
 20478-20479  _badwords_path
 28662-28671  _brain_growth_loop
 11557-11584  _brain_growth_snapshot
  2397-2417   _brain_hint_delay
 11549-11551  _brain_history_for
  6833-6861   _brain_notify
 11526-11547  _brain_record
 11553-11555  _brain_stream_recent
 14864-14881  _browser_push
  6877-6964   _build_daily_summary
  2900-3080   _build_native_cmd
 18798-18985  _build_restream_cmd
  3124-3157   _build_ytdlp_cmd
 25904-25911  _cached_probe
  5655-5682   _can_stop_tracking
  1797-1819   _capture_set_cookies
 16041-16044  _cfg_get
 16047-16049  _cfg_set
 24747-24782  _channel_set_all
 18048-18051  _chat_connected
 18054-18070  _chat_disconnected
  8907-8918   _chat_is_forum
 18090-18092  _chat_sanitize
 18094-18103  _chat_src_ok
 18033-18045  _chat_stat
 18073-18076  _chat_stats_snapshot
  3686-3697   _check_ai_alive_sync
  3700-3712   _check_ai_models_sync
 25913-25926  _check_redis_alive_sync
 25928-25948  _check_redis_version_sync
 14742-14755  _ci_key
 12156-12199  _classify_pool_anonymity
 12202-12219  _classify_pool_anonymity_bg
   775-779    _claude_chat_sync_metered
 10452-10459  _client_ip
 29217-29244  _clip_prune
 29247-29257  _clip_recfile_for
 29773-29779  _clip_should_velocity
 29298-29380  _clip_to_discord
  3584-3593   _close_ai_session
 30297-30312  _cohost_broadcast
 30279-30283  _cohost_cfg
 30338-30350  _cohost_fire_highlight
 30286-30294  _cohost_gate
 30315-30335  _cohost_highlight
 29429-29463  _community_events_loop
 11380-11382  _conv_messages
  7257-7297   _cookie_alarm_loop
  1869-1873   _cookie_autorefresh_info
  1774-1778   _cookie_header
 14914-14946  _cpu_load_snapshot
  3894-3906   _create_index_safe
 13241-13256  _creator_activity
 13297-13320  _creator_dossier_generate
 13259-13270  _creator_facts_line
 26165-26271  _crowdsec_status
 26131-26162  _crowdsec_via_lapi
 25996-26014  _cscli_bin
 26020-26033  _cscli_path
  7150-7175   _daily_summary_loop
 26051-26068  _darf_journal_lesen
 11047-11075  _dashboard_track_group
 28674-28694  _db_maintenance_loop
  7122-7147   _db_vacuum_loop
 20613-20637  _detect_foreign_ad
  1356-1367   _diag_path_owner
 22008-22052  _director_finalize
 22819-22826  _director_for
 21957-22005  _director_mark
 29667-29702  _disc_automod_check
 29640-29646  _disc_state_get
 29649-29656  _disc_state_set
 26714-26727  _discord_guild_filesize_bytes
 26913-26922  _discord_invite
 29601-29637  _discord_live_thread
 22159-22171  _discord_notify
 26814-26839  _discord_ops_alert
 29499-29597  _discord_post_user
 26978-28659  _discord_run_once
 26852-26910  _discord_start
 29188-29194  _discord_stop
 26735-26737  _discord_upload_limit_label
 26730-26732  _discord_upload_limit_mb
  7178-7252   _disk_alarm_loop
 31679-31728  _disk_autoclean
 31731-31744  _disk_guard_loop
 31671-31676  _disk_pct
 25060-25063  _donations_unknown_count
 18407-18409  _drawtext_chain
 15493-15495  _dump_all_threads
 12081-12145  _enrich_proxies_with_geo
  2014-2058   _ensure_cookie_file_netscape
 26925-26975  _ensure_discord_invite
 29394-29426  _ensure_error_channel
  8966-8969   _ensure_notify_topic
 12324-12361  _ensure_proxy_ready
  8920-8947   _ensure_topic
   638-640    _env_int
   643-645    _env_int_range
 29466-29496  _error_channel_loop
 22203-22216  _event_webhook
 17341-17347  _evo_build_dir
 17350-17357  _evo_version
 17633-17714  _evolution_cycle
 17366-17386  _evolution_llm_note
 17717-17727  _evolution_loop
 17389-17630  _evolution_write_build
  6275-6309   _extract_file_payload
  2146-2148   _extract_urls_from_streamurl_node
 26036-26043  _f2b_sudo_hint
 22239-22241  _faster_whisper_available
 20502-20514  _fetch_ldnoobw_de
 11970-11988  _fetch_proxy_list
 22653-22681  _fetch_tiktok_room_id
   709-712    _ff_cmd
 16164-16177  _ffmpeg_version_str
 18570-18575  _find_chromium
  3117-3121   _find_external_recorder
  2151-2153   _find_stream_urls
 16092-16117  _fire_webhooks
  8033-8042   _fork_safe
   790-799    _freeai_chat_sync_metered
 26086-26128  _geo_lookup_ips
  3573-3582   _get_ai_session
  7867-7907   _get_live_info
  2687-2694   _get_resolve_semaphore
  8268-8634   _handle_single_tracking
 31523-31525  _hb
 31528-31545  _hb_while
 18108-18110  _highlight_cfg
 18113-18142  _highlight_observe
 18578-18583  _htmlov_screenshot_cmd
 22397-22407  _httpx_proxy
 16125-16137  _in_quiet_hours
 32558-32589  _install_fast_eventloop
 10322-10376  _install_fast_json
 15498-15514  _install_faulthandler
 23512-23521  _intel_ensure_schema
 23559-23594  _intel_index_loop
 23533-23543  _intel_index_one
 23524-23530  _intel_semantic
  5644-5653   _is_authorized
  8198-8204   _is_dead
  2136-2138   _is_hevc
 26071-26077  _is_private_ip
  1520-1527   _is_process_running
  6863-6874   _is_quiet_hours
  1160-1169   _is_upload_window
 10411-10424  _json_error_handler
  7080-7110   _kick_broadcaster_id
 12747-12766  _kick_channel_live
  6997-7039   _kick_follower_count
 13825-13838  _kick_oauth_exchange
 13841-13843  _kick_oauth_page
 13784-13788  _kick_redirect_public
 13779-13781  _kick_redirect_source
 13771-13776  _kick_redirect_uri
  6982-6984   _kick_slug
 13791-13822  _kick_user_token
  3943-3946   _kind_from_filename
 16154-16159  _latest_popularity
 20524-20530  _learned_load
 20521-20522  _learned_path
 20532-20540  _learned_save
 23034-23064  _live_react_loop
 22830-23023  _live_react_worker
 21620-21631  _live_transcript_push
 23025-23032  _live_users
 22055-22099  _living_title_loop
 20481-20489  _load_banned_words_file
  1695-1768   _load_cookies_dict
 28869-28941  _local_backup_scan
 10393-10407  _log_5xx
 18993-19005  _looks_like_codec_err
 18988-18990  _looks_like_source_expired
  8114-8144   _loop_fehler
 15518-15527  _loop_heartbeat
 31493-31520  _loop_lag_monitor
 15637-15640  _loop_not_ready
 15530-15598  _loop_watchdog_thread
 21500-21514  _loyalty_add
 21491-21497  _loyalty_get
 21517-21525  _loyalty_top
 16538-16556  _manual_donations_rows
 16559-16561  _manual_donations_total
  8206-8207   _mark_dead
 12914-12943  _marketing_cfg
 12905-12911  _marketing_default_targets
 12900-12902  _marketing_enabled
 12957-12972  _marketing_flavor
 13027-13043  _marketing_loop
 12975-12985  _marketing_post_discord
 12988-13000  _marketing_post_telegram
 13003-13024  _marketing_publish
 12946-12950  _marketing_state_obj
 12953-12954  _marketing_state_save
 30200-30218  _maybe_handle_command
 31830-31854  _maybe_hype_clip
  3861-3884   _migrate_columns
 30477-30488  _mod_is_exempt
 30491-30496  _mod_warn_first
 30499-30502  _mod_warn_text
 17896-17904  _modlog
   913-915    _multistream_targets
  8045-8046   _nc_create_subprocess_exec
  8049-8050   _nc_create_subprocess_shell
 13138-13154  _news_cfg
 13125-13127  _news_enabled
 13192-13233  _news_facts
 13347-13369  _news_generate
 13552-13569  _news_loop
 13130-13135  _news_output_path
 13236-13238  _news_phrase
 13323-13344  _news_phrase_impl
 13167-13174  _news_read
 13157-13160  _news_state_obj
 13163-13164  _news_state_save
 13177-13189  _news_write
 17934-17936  _normalize_ingest
  2328-2345   _note_check_duration
  8960-8963   _notify_topic_name
 13735-13746  _oauth_redirect_env
 13762-13768  _oauth_redirect_source
 13749-13759  _oauth_redirect_uri
 21646-21654  _oracle_memories
 21912-21946  _oracle_memorize
 21657-21670  _oracle_persona
 21639-21643  _oracle_recent_text
 18233-18241  _ov_atomic_write
 18221-18227  _ov_bar
 20437-20449  _ov_clip_text
 18230-18231  _ov_oneline
 25071-25100  _overlay_push
 18524-18567  _overlay_render_size
 17995-17999  _overlay_session_reset
 25019-25022  _overlay_src_ok
 20600-20610  _own_invites
 16519-16535  _parse_eur
 18519-18521  _parse_size
 26279-26359  _parse_ssh_attacks
  7469-7502   _pause_resume_cmd
  1823-1867   _persist_refreshed_cookies
  1661-1693   _pick_checked_pull_proxy
 10488-10501  _pin_auth_value
 10547-10548  _pin_clear_fail
 10527-10530  _pin_locked
 10533-10544  _pin_note_fail
 10504-10524  _pin_ok
 24909-24911  _piper_available
 24874-24896  _piper_list_voices
 24916-24941  _piper_pick_model
 24953-25000  _piper_say
 24867-24871  _piper_voice_roots
 16054-16089  _post_json_threaded
 18498-18516  _probe_video_size
  1548-1565   _proc_is_recorder
 12068-12079  _proxy_geo_cache_put
 12295-12321  _proxy_pool_refresh_loop
  1627-1658   _proxy_report_recording
 15483-15485  _prune_stall_dumps
 13694-13732  _public_base_url
 13372-13493  _public_stats
 22174-22200  _push_notify
 10649-10651  _pwa_dir
 12039-12054  _quick_validate_proxy
 16120-16122  _quiet_hours_config
 10614-10647  _rate_guard
 21465-21471  _react_warn
  7953-7992   _reap_proc
  2368-2390   _record_check_outcome
   704-706    _redact_stream_urls
 12222-12292  _refresh_proxy_pool
 24899-24905  _resolve_piper_model
 14758-14773  _resolve_tracked_user
  2162-2252   _resolve_via_html
  2510-2664   _resolve_via_webcast_api_v2
  2727-2789   _resolve_via_ytdlp
 29819-29948  _resolve_youtube_ingest
 23103-23110  _restream_active_platforms
 17980-17991  _restream_active_sources
 22684-22783  _restream_chat_guardian
 18145-18217  _restream_chat_push
 17907-17919  _restream_enabled
 18586-18673  _restream_html_overlay_start
 18676-18689  _restream_html_overlay_stop
  1108-1110   _restream_layout_mode
 17945-17968  _restream_overlay_files
 23068-23100  _restream_platform_state
 23231-23266  _restream_resume_after_restart
 18737-18795  _restream_tts_enqueue_wav
 18460-18492  _restream_tts_feeder
 18457-18458  _restream_tts_fifo_path
 18692-18719  _restream_tts_start
 18721-18735  _restream_tts_stop
 23113-23228  _restream_verify_loop
 28834-28846  _retention_loop
 28793-28831  _retention_scan
  2472-2474   _room_is_abo
  6313-6430   _run_ai_call
 15621-15634  _run_async_from_flask
 26080-26083  _run_priv
 32546-32554  _run_selfcheck_and_exit
 28849-28860  _s3_client
  8209-8255   _safe_send
  4796-4812   _sample_net_throughput
 20491-20499  _save_banned_words_file
  2420-2447   _schedule_next_check
 28750-28790  _scheduler_loop
  3887-3891   _schema_pk
 15642-15647  _scraper_session
 30505-30544  _screen_full
 14151-14188  _sec_headers
  2141-2143   _select_stream_from_data_section
 32359-32543  _selfcheck
  8972-9006   _send_live_notice
  1183-1187   _should_defer_upload
 29260-29295  _shrink_for_discord
 10654-10666  _sicheres_ziel
 31751-31768  _sign_health_check
 31771-31790  _sign_health_loop
  8062-8073   _spawn
  8076-8106   _spawn_from_flask
 26403-26406  _st_befund
 22409-22650  _start_chat_listener
 15601-15618  _start_loop_watchdog
 13517-13543  _stats_loop
 13496-13499  _stats_output_path
 13502-13514  _stats_write
  8702-8716   _storage_cleanup_loop
 31810-31817  _story_for
  3179-3185   _stream_url_expiry
  3194-3200   _stream_url_is_fresh
  3187-3192   _stream_url_ttl
 20564-20571  _streamer_persona_get
 20546-20552  _streamer_personas_load
 20543-20544  _streamer_personas_path
 20554-20562  _streamer_personas_save
 18412-18416  _studio_chain
 28966-29088  _system_backup
 29091-29119  _system_backup_loop
 11991-12030  _test_proxy
 12788-12797  _testpush_cfg
 12800-12817  _testpush_exec
 12769-12785  _testpush_resolve_live
  8879-8889   _tg_topics_load_into_mem
  8876-8877   _tg_topics_path
  8891-8898   _tg_topics_save
 25613-25661  _tiktok_account_exists
 10462-10470  _token_ok
  8901-8905   _topic_forget
 16140-16151  _tracking_max_duration
  1414-1437   _try_attach_file_handler
 24943-24951  _tts_cleanup
 12673-12676  _tunnel_effective
 24369-24422  _twitch_channel_status
 30547-30690  _twitch_chat_loop
 30361-30464  _twitch_eventsub_loop
 17061-17064  _twitch_oauth_page
  1206-1219   _upload_queue_add
  1230-1232   _upload_queue_count
  1189-1198   _upload_queue_load
  1179-1181   _upload_queue_path
  1221-1228   _upload_queue_remove
  1200-1204   _upload_queue_save
  1234-1272   _upload_window_loop
  7926-7933   _uptime_s
 17922-17931  _url_host
   684-701    _url_ohne_zugang
   768-772    _usage_record_claude
  8147-8191   _verbindung_verloren
  7042-7070   _viewer_sample_loop
  7112-7119   _viewer_stats
 10551-10554  _wants_html
  7936-7950   _warn_empty_env
 31566-31661  _watchdog_loop
 30102-30110  _wchat_thank_ok
 22243-22273  _whisper_get_model
  8023-8030   _whisper_native_section
 21452-21458  _whisper_pool
 22342-22371  _whisper_segments
 22275-22339  _whisper_transcribe
 18243-18405  _write_restream_overlay
 30718-30791  _youtube_api_chat_loop
 24425-24528  _youtube_api_status
 24531-24598  _youtube_channel_status
 30794-30951  _youtube_chat_loop
 29954-29967  _youtube_restream_autoconfig
 29970-29994  _youtube_restream_autoconfig_inner
 30060-30088  _youtube_send
 24703-24744  _youtube_set_channel
 29997-30031  _yt_access_token
 30034-30049  _yt_live_chat_id
 30711-30715  _yt_oauth_configured
 30055-30057  _yt_sendrate_cfg
 30693-30708  _yt_timeout
  2711-2712   _ytdlp_detect_available
  2714-2725   _ytdlp_note_result
 15488-15490  _zombie_child_count
  7803-7827   about
  4062-4066   add_ai_log_entry
  3979-3982   add_archive_entry
  4909-4924   add_archive_rule
  4491-4525   add_recording
  4152-4169   add_tracking
  4586-4603   add_tracking_tag
  6433-6466   ai
  3726-3765   ai_chat
  3799-3809   ai_history_append
  3811-3816   ai_history_clear
  3788-3797   ai_history_load
  3773-3786   ai_rate_limit_check
  6495-6503   aireset
 21783-21802  azrael_chat
 30956-31078  brain_cmd
  3203-3387   build_recording_cmd
  4172-4249   bulk_add_trackings
  7300-7359   bulkadd
  8719-8859   check_all_trackings
  4336-4348   claim_live_transition
 20640-21395  class KickModerator
 19008-20324  class RestreamManager
 12406-12448  classify_proxy_anonymity
  6541-6739   cleanup
  5504-5545   cleanup_old_recordings
  4482-4489   clear_recording
 29705-29770  clip_moment
  5057-5100   cluster_failures
  4740-4789   compute_storage_forecast
  7422-7466   cookies_cmd
  5346-5352   cookies_days_old
  4143-4149   count_trackings_for_chat
  4049-4060   decide_preferred_recorder
  3989-3992   delete_archive_entry
  4926-4934   delete_archive_rule
  5970-6117   diag
 31190-31251  einnahmen_cmd
  4734-4737   find_recordings_by_fingerprint
  4010-4026   finish_recording_attempt
  4281-4291   get_all_active_trackings
  4088-4091   get_all_checks
  4527-4530   get_all_recordings
  4628-4638   get_all_tags_with_counts
  4711-4714   get_annotations_for_recording
  3984-3987   get_archive_entry
  4704-4707   get_bookmarked_recordings
  1890-2007   get_cookie_health
  4577-4583   get_event_log
  4033-4047   get_last_recording_attempt
  2792-2897   get_live_status
  5260-5263   get_manual_recordings
  4719-4722   get_or_compute_inspect_sync
  5580-5624   get_outcome_breakdown
  4685-4693   get_priority_poll_interval
  4887-4896   get_profile_snapshots
  4068-4078   get_recent_ai_log
  4028-4031   get_recent_recording_attempts
  4532-4535   get_recording_by_id
  4697-4700   get_recording_note
  3521-3544   get_redis
  4119-4135   get_stats
  5471-5502   get_storage_stats
  4618-4626   get_tags_for_tracking
  5027-5041   get_tiktok_status_distribution
  4672-4683   get_tracking_priority
  4350-4359   get_tracking_state
  4277-4279   get_trackings_for_group
  5276-5279   get_trash_recordings
  9627-10290  handle_recording_finished
  3909-3934   init_db
  5394-5448   inspect_stream_url
 25066-25068  is_revenue_platform
  4899-4907   list_archive_rules
  5774-5812   live
  8258-8266   live_check_worker
  3596-3630   llm_chat
  3653-3681   llm_chat_sync
  3638-3650   llm_list_models
  4543-4569   log_event
  1482-1515   log_recording_failure
  7616-7665   logs_cmd
 31858-32349  main
  6469-6492   on_ai_media
  7742-7768   on_ai_reply
  7771-7800   on_azrael_mention
  7832-7862   on_callback
 21805-21909  oracle_handle
  7505-7508   pause_tracking
  5634-5639   profile_keyboard
  5355-5391   quick_restart_tracking
  7567-7613   quota
  8636-8699   reaper_loop
  5023-5025   record_tiktok_status
  6508-6538   recstatus
  3546-3554   redis_get_json
  3556-3562   redis_set_json
  4251-4275   remove_tracking
  4605-4616   remove_tracking_tag
 31254-31264  report_cmd
 12451-12453  report_proxy_result
  2255-2282   resolve_tiktok_live_stream
  5271-5274   restore_recording
  7511-7514   resume_tracking
  4937-5017   run_archive_rules
 31267-31473  run_bot
 15410-15457  run_flask
  4815-4860   sample_bandwidth_for_active
  4866-4885   save_profile_snapshot
  4080-4086   save_tiktok_check
  4474-4480   set_recording_file
  4294-4332   set_tracking_paused
  4641-4670   set_tracking_priority
  5266-5269   soft_delete_recording
  9012-9625   split_and_send_video
  5687-5729   start
  3994-4008   start_recording_attempt
  6742-6780   stats
  5241-5258   stop_manual_recording
  7517-7564   stoprec
  6967-6975   summary_cmd
  7668-7739   sysres
  6119-6263   teststream
  5731-5772   tiktok
  7362-7419   topusers
  5849-5906   track
  5814-5846   track_exact
  5920-5968   tracklist
  5107-5239   trigger_manual_recording
  4435-4472   try_acquire_recording_lock
  5282-5341   universal_search
  5908-5918   untrack
 31081-31187  update_cmd
  4729-4732   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           class MarketingConfig, class MarketingState, compose, has_content, next_due_ts, should_post, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                build_items, class NewsConfig, class NewsState, item_id, merge, render_json, should_generate
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
trackingdb.py          claim_transition, get_state
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
