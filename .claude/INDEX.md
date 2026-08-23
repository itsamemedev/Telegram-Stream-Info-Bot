# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (255)

```
 10465  GET              /                                                dashboard
 15355  GET              /api/abo/status                                  api_abo_status
 10564  GET              /api/active-recordings                           api_active_recordings
 15430  GET              /api/activity-pulse                              api_activity_pulse
 14783  GET              /api/ai-log                                      api_ai_log
 10962  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 15190  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 22969  GET/POST         /api/audio/config                                api_audio_config
 22999  POST             /api/audio/testtone                              api_audio_testtone
 15296  GET/POST         /api/auto-archive-rules                          api_archive_rules
 15320  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 15324  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12240  GET              /api/automation/status                           api_automation_status
 12262  POST             /api/automation/toggle                           api_automation_toggle
 13988  GET              /api/azrael/agents                               api_azrael_agents
 12143  POST             /api/azrael/ask                                  api_azrael_ask
 23205  GET/POST         /api/azrael/context                              api_azrael_context
 13615  GET              /api/azrael/core                                 api_azrael_core
 23339  POST             /api/azrael/live_pause                           api_azrael_live_pause
 23329  GET              /api/azrael/live_status                          api_azrael_live_status
 23347  POST             /api/azrael/live_test                            api_azrael_live_test
 13997  GET              /api/azrael/memories                             api_azrael_memories
 23395  POST             /api/azrael/persona                              api_azrael_persona_set
 23386  GET              /api/azrael/personas                             api_azrael_personas
 23423  GET              /api/azrael/piper_status                         api_azrael_piper_status
 23178  POST             /api/azrael/react                                api_azrael_react
 23214  GET              /api/azrael/reaction                             api_azrael_reaction
 23366  GET              /api/azrael/reactions                            api_azrael_reactions
 23416  GET              /api/azrael/transcript                           api_azrael_transcript
 23301  POST             /api/azrael/tts_test                             api_azrael_tts_test
 23276  GET              /api/azrael/voices                               api_azrael_voices
 23440  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11057  GET              /api/backoff-watch                               api_backoff_watch
 14554  POST             /api/backup/run                                  api_backup_run
 14520  GET              /api/backup/status                               api_backup_status
 14509  POST             /api/backup/system                               api_backup_system
 15262  GET              /api/bandwidth/live                              api_bandwidth_live
 15175  GET              /api/bookmarks                                   api_bookmarks_list
 11320  GET              /api/brain                                       api_brain
 11257  GET              /api/brain/alarms                                api_brain_alarms
 11242  GET              /api/brain/creator                               api_brain_creator
 11219  GET              /api/brain/graph                                 api_brain_graph
 11280  GET              /api/brain/growth                                api_brain_growth
 10061  GET              /api/brain/health                                api_brain_health
 23921  GET              /api/channel/categories                          api_channel_categories
 23927  POST             /api/channel/set                                 api_channel_set
 23737  GET              /api/channels/status                             api_channels_status
 22570  POST             /api/chat/send                                   api_chat_send
 14255  GET              /api/chat/send_status                            api_chat_send_status
 10545  GET              /api/checks                                      api_checks
 23242  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 23225  GET              /api/clips                                       api_clips
 23258  POST/DELETE      /api/clips/clear                                 api_clips_clear
 22844  GET              /api/cohost                                      api_cohost
 22856  POST             /api/cohost/config                               api_cohost_config
 15994  GET              /api/community/stats                             api_community_stats
 24921  POST             /api/config/restore                              api_config_restore
 24906  GET              /api/config/snapshot                             api_config_snapshot
 15453  GET              /api/cookies/age                                 api_cookies_age
 10612  GET              /api/cookies/health                              api_cookies_health
 10619  POST             /api/cookies/update                              api_cookies_update
 24872  GET              /api/data/export                                 api_data_export
 16504  GET              /api/db/export                                   api_db_export
 16531  POST             /api/db/import                                   api_db_import
 16491  GET              /api/db/summary                                  api_db_summary
 22770  GET              /api/debug/threads                               api_debug_threads
 25807  GET              /api/defense/attacks                             api_defense_attacks
 25774  GET              /api/defense/crowdsec                            api_defense_crowdsec
 25792  GET              /api/defense/fail2ban                            api_defense_fail2ban
 25498  GET              /api/defense/overview                            api_defense_overview
 14616  POST             /api/discord/announce                            api_discord_announce
 14344  GET              /api/discord/clips_week                          api_discord_clips_week
 14560  GET              /api/discord/community                           api_discord_community
 14283  GET              /api/discord/invite                              api_discord_invite
 13746  GET              /api/discord/overview                            api_discord_overview
 13832  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16071  POST             /api/donations/add                               api_donations_add
 16104  GET              /api/donations/manual                            api_donations_manual
 16112  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16007  POST             /api/donations/reset                             api_donations_reset
 16128  GET              /api/donations/summary                           api_donations_summary
 15244  GET              /api/events                                      api_events
 14391  GET              /api/events/stream                               api_events_stream
 17159  GET              /api/evolution/changelog                         api_evolution_changelog
 17144  GET              /api/evolution/history                           api_evolution_history
 17084  GET              /api/evolution/learned                           api_evolution_learned
 17106  GET              /api/evolution/proposals                         api_evolution_proposals
 17127  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17074  POST             /api/evolution/run                               api_evolution_run
 17174  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17039  GET              /api/evolution/status                            api_evolution_status
 16338  GET              /api/finanzamt/entries                           api_finanzamt_entries
 16358  POST             /api/finanzamt/entry                             api_finanzamt_add
 16385  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15257  GET              /api/forecast/storage                            api_forecast_storage
 12278  GET              /api/freeai/status                               api_freeai_status
 13688  GET              /api/health                                      api_health
 15275  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15271  GET              /api/heatmap/recordings                          api_heatmap_recordings
 22893  GET              /api/highlights                                  api_highlights
 22905  POST             /api/highlights/config                           api_highlights_config
 23778  GET              /api/kick/channel                                api_kick_channel
 23799  POST             /api/kick/channel                                api_kick_channel_set
 13415  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13483  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13461  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13400  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13440  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23017  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23086  POST             /api/kickmod/config                              api_kickmod_config
 23131  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23145  GET              /api/kickmod/learned                             api_kickmod_learned
 23172  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23152  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 23483  POST             /api/kickmod/say                                 api_kickmod_say
 23459  POST             /api/kickmod/start                               api_kickmod_start
 23057  GET              /api/kickmod/status                              api_kickmod_status
 23470  POST             /api/kickmod/stop                                api_kickmod_stop
 10397  POST             /api/login                                       dashboard_login_submit
 15979  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12693  POST             /api/marketing/config                            api_marketing_config
 12718  GET              /api/marketing/preview                           api_marketing_preview
 12728  POST             /api/marketing/send-now                          api_marketing_send_now
 12667  GET              /api/marketing/status                            api_marketing_status
 12685  POST             /api/marketing/toggle                            api_marketing_toggle
 22920  GET              /api/moderation/feed                             api_moderation_feed
 13246  POST             /api/news/config                                 api_news_config
 13212  GET              /api/news/creators                               api_news_creators
 13223  POST             /api/news/creators/generate                      api_news_creators_generate
 13288  POST             /api/news/generate-now                           api_news_generate_now
 13283  GET              /api/news/items                                  api_news_items
 13274  GET              /api/news/preview                                api_news_preview
 13193  GET              /api/news/status                                 api_news_status
 13238  POST             /api/news/toggle                                 api_news_toggle
 15836  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14220  GET              /api/notify/status                               api_notify_status
 14231  POST             /api/notify/test                                 api_notify_test
 14206  GET              /api/ops/audit                                   api_ops_audit
 15907  GET              /api/ops/db-stats                                api_ops_db_stats
 15935  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14012  GET              /api/ops/errors                                  api_ops_errors
 15856  GET              /api/ops/healthcheck                             api_ops_healthcheck
 16586  GET              /api/ops/log-tail                                api_ops_log_tail
 12123  GET              /api/ops/logtail                                 api_ops_logtail
 13953  GET              /api/ops/metrics                                 api_ops_metrics
 13936  GET              /api/ops/resource_history                        api_ops_resource_history
 16560  GET              /api/ops/version                                 api_ops_version
 10815  GET              /api/outcomes                                    api_outcomes
 24402  POST             /api/overlay/config                              api_overlay_config
 24389  POST             /api/overlay/event                               api_overlay_event
 24294  GET              /api/overlay/state                               api_overlay_state
 10848  GET              /api/profile/<username>                          api_profile
 15461  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15283  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15409  GET              /api/proxy/heatmap                               api_proxy_heatmap
 15386  GET              /api/proxy/trend                                 api_proxy_trend
 13167  GET              /api/public/stats                                api_public_stats
 10499  GET              /api/pulse                                       api_pulse
 14807  GET              /api/recording-attempts                          api_recording_attempts
 22505  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 22483  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 22524  POST             /api/restream/<int:rid>/start                    api_restream_start
 22791  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 24256  GET              /api/restream/chatfeed                           api_restream_chatfeed
 22459  POST             /api/restream/create                             api_restream_create
 13491  GET              /api/restream/deck                               api_restream_deck
 12214  GET              /api/restream/health                             api_restream_health
 24278  POST             /api/restream/layout                             api_restream_layout
 22432  GET              /api/restream/list                               api_restream_list
 12187  POST             /api/restream/report                             api_restream_report
 22804  POST             /api/restream/start_all                          api_restream_start_all
 22830  POST             /api/restream/stop_all                           api_restream_stop_all
 12441  GET              /api/restream/testpush                           api_testpush_status
 12466  POST             /api/restream/testpush                           api_testpush_run
 16244  GET              /api/restream/verify                             api_restream_verify
 14322  GET              /api/retention/preview                           api_retention_preview
 14331  POST             /api/retention/run                               api_retention_run
 24987  POST             /api/schedule/add                                api_schedule_add
 24977  GET              /api/schedule/list                               api_schedule_list
 25012  POST             /api/schedule/remove                             api_schedule_remove
 15160  GET              /api/search                                      api_search
 25545  GET              /api/selftest                                    api_selftest
 22541  GET              /api/shield/stats                                api_shield_stats
 10518  GET              /api/stats                                       api_stats
 15424  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 15351  GET              /api/stats/tiktok-status                         api_tiktok_status
 24952  GET              /api/stats/timeline                              api_stats_timeline
 10586  GET              /api/storage                                     api_storage
 10593  POST             /api/storage/cleanup                             api_storage_cleanup
 15337  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12164  GET              /api/stream/timeline                             api_stream_timeline
 13820  GET              /api/stream/transcript                           api_stream_transcript
 24620  GET              /api/streamer/compare                            api_streamer_compare
 24819  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14296  GET              /api/streamer/detail                             api_streamer_detail
 24844  GET              /api/streamer/digest/<username>                  api_streamer_digest
 24724  GET              /api/streamer/dormant                            api_streamer_dormant
 24800  GET              /api/streamer/exists/<username>                  api_streamer_exists
 24679  GET              /api/streamer/journal/<username>                 api_streamer_journal
 24644  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 24704  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13655  GET              /api/streamers/wall                              api_streamers_wall
 10735  GET              /api/summary/preview                             api_summary_preview
 14872  GET              /api/system                                      api_system
 16192  GET              /api/system/check_timing                         api_check_timing
 16472  GET              /api/system/config_drift                         api_config_drift
 13856  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14067  GET              /api/system/preflight                            api_system_preflight
 14193  GET              /api/system/preflight_history                    api_system_preflight_history
 14456  GET              /api/system/resilience                           api_system_resilience
 15195  GET              /api/tags                                        api_tags_list
 10559  GET              /api/top                                         api_top
 12097  GET              /api/trackings                                   api_trackings
 15725  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 15758  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15231  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 15444  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 15787  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15217  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 14646  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 14693  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 14722  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 14704  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10752  POST             /api/trackings/bulk                              api_trackings_bulk
 14661  GET              /api/trackings/export                            api_trackings_export
 15199  GET              /api/trackings/tags-map                          api_trackings_tags_map
 15499  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11112  GET              /api/trend-7d                                    api_trend_7d
 23290  GET              /api/tts/<fn>                                    api_tts_file
 12321  POST             /api/tunnel/set                                  api_tunnel_set
 12300  GET              /api/tunnel/status                               api_tunnel_status
 12332  POST             /api/tunnel/test                                 api_tunnel_test
 12313  POST             /api/tunnel/toggle                               api_tunnel_toggle
 16444  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 16421  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 16403  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 24430  GET              /api/upload_window                               api_upload_window
 10829  GET              /api/userstats                                   api_userstats
 13299  GET              /api/version                                     api_version
 16300  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 16321  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 16285  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16269  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 29225  GET              /api/youtube/sendrate                            api_youtube_sendrate
 14845  GET              /archive/<int:eid>/download                      archive_download
 14902  GET              /download/<int:recording_id>                     download
 14768  GET              /health                                          health
 22739  GET              /healthz                                         healthz
 10386  GET              /login                                           dashboard_login_page
 10420  GET              /logout                                          dashboard_logout
 10427  GET              /manifest.webmanifest                            pwa_manifest
 13884  GET              /metrics                                         api_prometheus_metrics
 24239  GET              /overlay                                         overlay_page
 10451  GET              /pwa-icon-<variant>.png                          pwa_icon
 10437  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (90)

```
   966  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   706  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   837  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   817  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   855  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   779  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   319  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   330  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   340  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   363  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   370  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   381  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   514  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   612  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1204  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1236  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   303  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   919  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   899  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1072  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1120  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1171  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1030  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   874  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
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
 26250  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 26709  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 26341  /assign_role            Rolle/Gruppe einem Mitglied geben
 26387  /ban                    Mitglied bannen
 27041  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 26965  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 27005  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 26990  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 26832  /clips                  Letzte Highlight-Clips eines Users
 26302  /create_category        Kategorie anlegen
 26271  /create_channel         Text-Channel anlegen (optional in Kategorie)
 26330  /create_group           Nutzergruppe (= Rolle) anlegen
 26313  /create_role            Rolle / Nutzergruppe anlegen
 26287  /create_voice           Voice-Channel anlegen
 26623  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 26739  /event                  Community-Event ankündigen (Admin) — mit Countdown
 26782  /events                 Kommende Community-Events anzeigen
 26878  /follow                 Bei Live-Gang eines Streamers gepingt werden
 26862  /help                   Alle Bot-Befehle anzeigen
 26376  /kick                   Mitglied kicken
 26605  /leaderboard            Top-10 der Community nach XP
 26818  /livenow                Welche getrackten User sind gerade live
 26848  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 26679  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 26411  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 26591  /rank                   Dein Level und Rang anzeigen
 26805  /recstatus              Aktuell laufende Aufnahmen
 26352  /remove_role            Rolle/Gruppe entfernen
 26264  /restream_status        Restream-Status
 26363  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 26556  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 26574  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 26904  /stats                  Statistik zu einem getrackten Streamer
 26176  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 27200  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 27097  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 27073  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 26398  /timeout                Mitglied stummschalten (Minuten)
 26976  /topstreamers           Rangliste der Streamer nach Aufnahmen
 26206  /track                  TikTok-User tracken
 26190  /tracklist              Getrackte TikTok-User dieses Servers
 26893  /unfollow               Live-Pings für einen Streamer abbestellen
 26239  /untrack                TikTok-User nicht mehr tracken
 26926  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 26950  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 27684  on_member_join
 27646  on_message
 27287  on_raw_reaction_add
 27719  on_ready
```

## Top-Level-Symbole in bot_v37.py (551 Funktionen, 2 Klassen)

```
  2396-2397   _abo_key
  2417-2435   _abo_probe_dump
 25087-25097  _active_recorder_sync
 19745-19752  _ad_allowlist
 20858-20864  _agent_for
 25099-25117  _ai_calls_total_sync
 20867-20883  _ai_telemetry
 21365-21383  _alert
 27832-27882  _alert_monitor_loop
 28256-28318  _announce_loop
  3338-3341   _anthropic_key
  3348-3350   _anthropic_model
 10189-10192  _arg_int
  2388-2393   _as_dict
 17756-17761  _audio_cfg
 21519-21541  _audio_tap_cmd
 10322-10333  _auth_cookie
 10289-10318  _auth_guard
  1544-1549   _auto_on
 22408-22426  _auto_restream_loop
 29386-29401  _azrael_broadcast_reply
 29286-29308  _azrael_chat_reply
 29269-29283  _azrael_chat_should_reply
 12893-12911  _azrael_creator_take
 29314-29316  _azrael_gate_cfg
 20888-20902  _azrael_live_state
 24138-24152  _azrael_overlay_state
 21248-21302  _azrael_proactive_loop
 20707-20763  _azrael_reaction_to_chats
 29319-29326  _azrael_reply_all_chats
 29256-29266  _azrael_self_names
 29354-29383  _azrael_send_to
 20905-20926  _azrael_system
 27996-27999  _backup_active
 28077-28090  _backup_loop
 19633-19634  _badwords_path
 27797-27806  _brain_growth_loop
 11188-11215  _brain_growth_snapshot
  2324-2344   _brain_hint_delay
 11180-11182  _brain_history_for
  6760-6788   _brain_notify
 11157-11178  _brain_record
 11184-11186  _brain_stream_recent
 14370-14387  _browser_push
  6804-6891   _build_daily_summary
  2827-3007   _build_native_cmd
 18104-18291  _build_restream_cmd
  3051-3084   _build_ytdlp_cmd
 25039-25046  _cached_probe
  5582-5609   _can_stop_tracking
  1724-1746   _capture_set_cookies
 15547-15550  _cfg_get
 15553-15555  _cfg_set
 23882-23917  _channel_set_all
 17354-17357  _chat_connected
 17360-17376  _chat_disconnected
  8786-8797   _chat_is_forum
 17396-17398  _chat_sanitize
 17400-17409  _chat_src_ok
 17339-17351  _chat_stat
 17379-17382  _chat_stats_snapshot
  3613-3624   _check_ai_alive_sync
  3627-3639   _check_ai_models_sync
 25048-25061  _check_redis_alive_sync
 25063-25083  _check_redis_version_sync
 11787-11830  _classify_pool_anonymity
 11833-11850  _classify_pool_anonymity_bg
   754-758    _claude_chat_sync_metered
 10214-10221  _client_ip
 28350-28377  _clip_prune
 28380-28390  _clip_recfile_for
 28906-28912  _clip_should_velocity
 28431-28513  _clip_to_discord
  3511-3520   _close_ai_session
 29430-29445  _cohost_broadcast
 29412-29416  _cohost_cfg
 29471-29483  _cohost_fire_highlight
 29419-29427  _cohost_gate
 29448-29468  _cohost_highlight
 28562-28596  _community_events_loop
 11011-11013  _conv_messages
  7184-7224   _cookie_alarm_loop
  1796-1800   _cookie_autorefresh_info
  1701-1705   _cookie_header
 14420-14452  _cpu_load_snapshot
  3821-3833   _create_index_safe
 12861-12876  _creator_activity
 12917-12940  _creator_dossier_generate
 12879-12890  _creator_facts_line
 25300-25406  _crowdsec_status
 25266-25297  _crowdsec_via_lapi
 25131-25149  _cscli_bin
 25155-25168  _cscli_path
  7077-7102   _daily_summary_loop
 25186-25203  _darf_journal_lesen
 27809-27829  _db_maintenance_loop
  7049-7074   _db_vacuum_loop
 19768-19792  _detect_foreign_ad
  1301-1312   _diag_path_owner
 21154-21198  _director_finalize
 21965-21972  _director_for
 21103-21151  _director_mark
 28800-28835  _disc_automod_check
 28773-28779  _disc_state_get
 28782-28789  _disc_state_set
 25849-25862  _discord_guild_filesize_bytes
 26048-26057  _discord_invite
 28734-28770  _discord_live_thread
 21305-21317  _discord_notify
 25949-25974  _discord_ops_alert
 28632-28730  _discord_post_user
 26113-27794  _discord_run_once
 25987-26045  _discord_start
 28321-28327  _discord_stop
 25870-25872  _discord_upload_limit_label
 25865-25867  _discord_upload_limit_mb
  7105-7179   _disk_alarm_loop
 30699-30748  _disk_autoclean
 30751-30764  _disk_guard_loop
 30691-30696  _disk_pct
 24195-24198  _donations_unknown_count
 17713-17715  _drawtext_chain
 14999-15001  _dump_all_threads
 11712-11776  _enrich_proxies_with_geo
  1941-1985   _ensure_cookie_file_netscape
 26060-26110  _ensure_discord_invite
 28527-28559  _ensure_error_channel
 11955-11992  _ensure_proxy_ready
  8799-8822   _ensure_topic
   637-639    _env_int
   642-644    _env_int_range
 28599-28629  _error_channel_loop
 21349-21362  _event_webhook
 16647-16653  _evo_build_dir
 16656-16663  _evo_version
 16939-17020  _evolution_cycle
 16672-16692  _evolution_llm_note
 17023-17033  _evolution_loop
 16695-16936  _evolution_write_build
  6202-6236   _extract_file_payload
  2073-2075   _extract_urls_from_streamurl_node
 25171-25178  _f2b_sudo_hint
 21385-21387  _faster_whisper_available
 19657-19669  _fetch_ldnoobw_de
 11601-11619  _fetch_proxy_list
 21799-21827  _fetch_tiktok_room_id
   688-691    _ff_cmd
 15670-15683  _ffmpeg_version_str
 17876-17881  _find_chromium
  3044-3048   _find_external_recorder
  2078-2080   _find_stream_urls
 15598-15623  _fire_webhooks
  7960-7969   _fork_safe
   769-778    _freeai_chat_sync_metered
 25221-25263  _geo_lookup_ips
  3500-3509   _get_ai_session
  7794-7834   _get_live_info
  2614-2621   _get_resolve_semaphore
  8148-8513   _handle_single_tracking
 30543-30545  _hb
 30548-30565  _hb_while
 17414-17416  _highlight_cfg
 17419-17448  _highlight_observe
 17884-17889  _htmlov_screenshot_cmd
 21543-21553  _httpx_proxy
 15631-15643  _in_quiet_hours
 31532-31563  _install_fast_eventloop
 10084-10138  _install_fast_json
 15004-15020  _install_faulthandler
 22651-22660  _intel_ensure_schema
 22698-22729  _intel_index_loop
 22672-22682  _intel_index_one
 22663-22669  _intel_semantic
  5571-5580   _is_authorized
  8078-8084   _is_dead
  2063-2065   _is_hevc
 25206-25212  _is_private_ip
  1447-1454   _is_process_running
  6790-6801   _is_quiet_hours
  1109-1118   _is_upload_window
 10173-10186  _json_error_handler
  7007-7037   _kick_broadcaster_id
 12367-12386  _kick_channel_live
  6924-6966   _kick_follower_count
 13378-13391  _kick_oauth_exchange
 13394-13396  _kick_oauth_page
 13337-13341  _kick_redirect_public
 13328-13334  _kick_redirect_source
 13314-13325  _kick_redirect_uri
  6909-6911   _kick_slug
 13344-13375  _kick_user_token
  3870-3873   _kind_from_filename
 15660-15665  _latest_popularity
 19679-19685  _learned_load
 19676-19677  _learned_path
 19687-19695  _learned_save
 22180-22210  _live_react_loop
 21976-22169  _live_react_worker
 20766-20777  _live_transcript_push
 22171-22178  _live_users
 21201-21245  _living_title_loop
 19636-19644  _load_banned_words_file
  1622-1695   _load_cookies_dict
 28002-28074  _local_backup_scan
 10155-10169  _log_5xx
 18299-18311  _looks_like_codec_err
 18294-18296  _looks_like_source_expired
  8041-8071   _loop_fehler
 15024-15033  _loop_heartbeat
 30513-30540  _loop_lag_monitor
 15143-15146  _loop_not_ready
 15036-15104  _loop_watchdog_thread
 20646-20660  _loyalty_add
 20637-20643  _loyalty_get
 20663-20671  _loyalty_top
 16044-16062  _manual_donations_rows
 16065-16067  _manual_donations_total
  8086-8087   _mark_dead
 12534-12563  _marketing_cfg
 12525-12531  _marketing_default_targets
 12520-12522  _marketing_enabled
 12577-12592  _marketing_flavor
 12647-12663  _marketing_loop
 12595-12605  _marketing_post_discord
 12608-12620  _marketing_post_telegram
 12623-12644  _marketing_publish
 12566-12570  _marketing_state_obj
 12573-12574  _marketing_state_save
 29333-29351  _maybe_handle_command
 30850-30874  _maybe_hype_clip
  3788-3811   _migrate_columns
 29608-29619  _mod_is_exempt
 29622-29627  _mod_warn_first
 29630-29633  _mod_warn_text
 17202-17210  _modlog
   890-892    _multistream_targets
  7972-7973   _nc_create_subprocess_exec
  7976-7977   _nc_create_subprocess_shell
 12758-12774  _news_cfg
 12745-12747  _news_enabled
 12812-12853  _news_facts
 12967-12989  _news_generate
 13172-13189  _news_loop
 12750-12755  _news_output_path
 12856-12858  _news_phrase
 12943-12964  _news_phrase_impl
 12787-12794  _news_read
 12777-12780  _news_state_obj
 12783-12784  _news_state_save
 12797-12809  _news_write
 17240-17242  _normalize_ingest
  2255-2272   _note_check_duration
 20792-20800  _oracle_memories
 21058-21092  _oracle_memorize
 20803-20816  _oracle_persona
 20785-20789  _oracle_recent_text
 17539-17547  _ov_atomic_write
 17527-17533  _ov_bar
 19592-19604  _ov_clip_text
 17536-17537  _ov_oneline
 24206-24235  _overlay_push
 17830-17873  _overlay_render_size
 17301-17305  _overlay_session_reset
 24154-24157  _overlay_src_ok
 19755-19765  _own_invites
 16025-16041  _parse_eur
 17825-17827  _parse_size
 25414-25494  _parse_ssh_attacks
  7396-7429   _pause_resume_cmd
  1750-1794   _persist_refreshed_cookies
  1588-1620   _pick_checked_pull_proxy
 10241-10246  _pin_auth_value
 10278-10279  _pin_clear_fail
 10258-10261  _pin_locked
 10264-10275  _pin_note_fail
 10249-10255  _pin_ok
 24044-24046  _piper_available
 24009-24031  _piper_list_voices
 24051-24076  _piper_pick_model
 24088-24135  _piper_say
 24002-24006  _piper_voice_roots
 15560-15595  _post_json_threaded
 17804-17822  _probe_video_size
  1475-1492   _proc_is_recorder
 11699-11710  _proxy_geo_cache_put
 11926-11952  _proxy_pool_refresh_loop
  1554-1585   _proxy_report_recording
 14989-14991  _prune_stall_dumps
 12992-13113  _public_stats
 21320-21346  _push_notify
 10380-10382  _pwa_dir
 11670-11685  _quick_validate_proxy
 15626-15628  _quiet_hours_config
 10345-10378  _rate_guard
 20611-20617  _react_warn
  7880-7919   _reap_proc
  2295-2317   _record_check_outcome
   683-685    _redact_stream_urls
 11853-11923  _refresh_proxy_pool
 24034-24040  _resolve_piper_model
  2089-2179   _resolve_via_html
  2437-2591   _resolve_via_webcast_api_v2
  2654-2716   _resolve_via_ytdlp
 28952-29081  _resolve_youtube_ingest
 22249-22256  _restream_active_platforms
 17286-17297  _restream_active_sources
 21830-21929  _restream_chat_guardian
 17451-17523  _restream_chat_push
 17213-17225  _restream_enabled
 17892-17979  _restream_html_overlay_start
 17982-17995  _restream_html_overlay_stop
  1057-1059   _restream_layout_mode
 17251-17274  _restream_overlay_files
 22214-22246  _restream_platform_state
 22370-22405  _restream_resume_after_restart
 18043-18101  _restream_tts_enqueue_wav
 17766-17798  _restream_tts_feeder
 17763-17764  _restream_tts_fifo_path
 17998-18025  _restream_tts_start
 18027-18041  _restream_tts_stop
 22259-22367  _restream_verify_loop
 27967-27979  _retention_loop
 27926-27964  _retention_scan
  2399-2401   _room_is_abo
  6240-6357   _run_ai_call
 15127-15140  _run_async_from_flask
 25215-25218  _run_priv
 31520-31528  _run_selfcheck_and_exit
 27982-27993  _s3_client
  8089-8135   _safe_send
  4723-4739   _sample_net_throughput
 19646-19654  _save_banned_words_file
  2347-2374   _schedule_next_check
 27885-27923  _scheduler_loop
  3814-3818   _schema_pk
 15148-15153  _scraper_session
 29636-29675  _screen_full
 13704-13741  _sec_headers
  2068-2070   _select_stream_from_data_section
 31333-31517  _selfcheck
  1132-1136   _should_defer_upload
 28393-28428  _shrink_for_discord
 30771-30788  _sign_health_check
 30791-30810  _sign_health_loop
  7989-8000   _spawn
  8003-8033   _spawn_from_flask
 25538-25541  _st_befund
 21555-21796  _start_chat_listener
 15107-15124  _start_loop_watchdog
 13137-13163  _stats_loop
 13116-13119  _stats_output_path
 13122-13134  _stats_write
  8581-8595   _storage_cleanup_loop
 30830-30837  _story_for
  3106-3112   _stream_url_expiry
  3121-3127   _stream_url_is_fresh
  3114-3119   _stream_url_ttl
 19719-19726  _streamer_persona_get
 19701-19707  _streamer_personas_load
 19698-19699  _streamer_personas_path
 19709-19717  _streamer_personas_save
 17718-17722  _studio_chain
 28099-28221  _system_backup
 28224-28252  _system_backup_loop
 11622-11661  _test_proxy
 12408-12417  _testpush_cfg
 12420-12437  _testpush_exec
 12389-12405  _testpush_resolve_live
  8758-8768   _tg_topics_load_into_mem
  8755-8756   _tg_topics_path
  8770-8777   _tg_topics_save
 24748-24796  _tiktok_account_exists
 10224-10232  _token_ok
  8780-8784   _topic_forget
 15646-15657  _tracking_max_duration
  1359-1382   _try_attach_file_handler
 24078-24086  _tts_cleanup
 12293-12296  _tunnel_effective
 23504-23557  _twitch_channel_status
 29678-29820  _twitch_chat_loop
 29494-29595  _twitch_eventsub_loop
 16465-16468  _twitch_oauth_page
  1155-1168   _upload_queue_add
  1179-1181   _upload_queue_count
  1138-1147   _upload_queue_load
  1128-1130   _upload_queue_path
  1170-1177   _upload_queue_remove
  1149-1153   _upload_queue_save
  1183-1221   _upload_window_loop
  7853-7860   _uptime_s
 17228-17237  _url_host
   747-751    _usage_record_claude
  6969-6997   _viewer_sample_loop
  7039-7046   _viewer_stats
 10282-10285  _wants_html
  7863-7877   _warn_empty_env
 30586-30681  _watchdog_loop
 29235-29243  _wchat_thank_ok
 21389-21419  _whisper_get_model
  7950-7957   _whisper_native_section
 20598-20604  _whisper_pool
 21488-21517  _whisper_segments
 21421-21485  _whisper_transcribe
 17549-17711  _write_restream_overlay
 29848-29921  _youtube_api_chat_loop
 23560-23663  _youtube_api_status
 23666-23733  _youtube_channel_status
 29924-30081  _youtube_chat_loop
 29087-29100  _youtube_restream_autoconfig
 29103-29127  _youtube_restream_autoconfig_inner
 29193-29221  _youtube_send
 23838-23879  _youtube_set_channel
 29130-29164  _yt_access_token
 29167-29182  _yt_live_chat_id
 29841-29845  _yt_oauth_configured
 29188-29190  _yt_sendrate_cfg
 29823-29838  _yt_timeout
  2638-2639   _ytdlp_detect_available
  2641-2652   _ytdlp_note_result
 14994-14996  _zombie_child_count
  7730-7754   about
  3989-3993   add_ai_log_entry
  3906-3909   add_archive_entry
  4836-4851   add_archive_rule
  4418-4452   add_recording
  4079-4096   add_tracking
  4513-4530   add_tracking_tag
  6360-6393   ai
  3653-3692   ai_chat
  3726-3736   ai_history_append
  3738-3743   ai_history_clear
  3715-3724   ai_history_load
  3700-3713   ai_rate_limit_check
  6422-6430   aireset
 20929-20948  azrael_chat
 30086-30208  brain_cmd
  3130-3314   build_recording_cmd
  4099-4176   bulk_add_trackings
  7227-7286   bulkadd
  8598-8738   check_all_trackings
  4263-4275   claim_live_transition
 19795-20541  class KickModerator
 18314-19479  class RestreamManager
 12037-12079  classify_proxy_anonymity
  6468-6666   cleanup
  5431-5472   cleanup_old_recordings
  4409-4416   clear_recording
 28838-28903  clip_moment
  4984-5027   cluster_failures
  4667-4716   compute_storage_forecast
  7349-7393   cookies_cmd
  5273-5279   cookies_days_old
  4070-4076   count_trackings_for_chat
  3976-3987   decide_preferred_recorder
  3916-3919   delete_archive_entry
  4853-4861   delete_archive_rule
  5897-6044   diag
 30211-30272  einnahmen_cmd
  4661-4664   find_recordings_by_fingerprint
  3937-3953   finish_recording_attempt
  4208-4218   get_all_active_trackings
  4015-4018   get_all_checks
  4454-4457   get_all_recordings
  4555-4565   get_all_tags_with_counts
  4638-4641   get_annotations_for_recording
  3911-3914   get_archive_entry
  4631-4634   get_bookmarked_recordings
  1817-1934   get_cookie_health
  4504-4510   get_event_log
  3960-3974   get_last_recording_attempt
  2719-2824   get_live_status
  5187-5190   get_manual_recordings
  4646-4649   get_or_compute_inspect_sync
  5507-5551   get_outcome_breakdown
  4612-4620   get_priority_poll_interval
  4814-4823   get_profile_snapshots
  3995-4005   get_recent_ai_log
  3955-3958   get_recent_recording_attempts
  4459-4462   get_recording_by_id
  4624-4627   get_recording_note
  3448-3471   get_redis
  4046-4062   get_stats
  5398-5429   get_storage_stats
  4545-4553   get_tags_for_tracking
  4954-4968   get_tiktok_status_distribution
  4599-4610   get_tracking_priority
  4277-4286   get_tracking_state
  4204-4206   get_trackings_for_group
  5203-5206   get_trash_recordings
  9442-10052  handle_recording_finished
  3836-3861   init_db
  5321-5375   inspect_stream_url
 24201-24203  is_revenue_platform
  4826-4834   list_archive_rules
  5701-5739   live
  8138-8146   live_check_worker
  3523-3557   llm_chat
  3580-3608   llm_chat_sync
  3565-3577   llm_list_models
  4470-4496   log_event
  1409-1442   log_recording_failure
  7543-7592   logs_cmd
 30878-31323  main
  6396-6419   on_ai_media
  7669-7695   on_ai_reply
  7698-7727   on_azrael_mention
  7759-7789   on_callback
 20951-21055  oracle_handle
  7432-7435   pause_tracking
  5561-5566   profile_keyboard
  5282-5318   quick_restart_tracking
  7494-7540   quota
  8515-8578   reaper_loop
  4950-4952   record_tiktok_status
  6435-6465   recstatus
  3473-3481   redis_get_json
  3483-3489   redis_set_json
  4178-4202   remove_tracking
  4532-4543   remove_tracking_tag
 30275-30285  report_cmd
 12082-12084  report_proxy_result
  2182-2209   resolve_tiktok_live_stream
  5198-5201   restore_recording
  7438-7441   resume_tracking
  4864-4944   run_archive_rules
 30288-30493  run_bot
 14916-14963  run_flask
  4742-4787   sample_bandwidth_for_active
  4793-4812   save_profile_snapshot
  4007-4013   save_tiktok_check
  4401-4407   set_recording_file
  4221-4259   set_tracking_paused
  4568-4597   set_tracking_priority
  5193-5196   soft_delete_recording
  8827-9440   split_and_send_video
  5614-5656   start
  3921-3935   start_recording_attempt
  6669-6707   stats
  5168-5185   stop_manual_recording
  7444-7491   stoprec
  6894-6902   summary_cmd
  7595-7666   sysres
  6046-6190   teststream
  5658-5699   tiktok
  7289-7346   topusers
  5776-5833   track
  5741-5773   track_exact
  5847-5895   tracklist
  5034-5166   trigger_manual_recording
  4362-4399   try_acquire_recording_lock
  5209-5268   universal_search
  5835-5845   untrack
  4656-4659   update_recording_fingerprint
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
recdiag.py             disconnect_analysis, url_refresh_stats
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
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, set_channel, status
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
